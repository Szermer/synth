"""
SSR-based response generation for synthetic personas.

This module integrates the Semantic Similarity Rating (SSR) methodology
for converting LLM text responses to realistic probability distributions
across rating scales.

Based on: "LLMs Reproduce Human Purchase Intent via Semantic Similarity
Elicitation of Likert Ratings" (Maier et al., 2025)
"""

import polars as po
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Union
import numpy as np
from semantic_similarity_rating import ResponseRater


class SSRResponseGenerator:
    """
    Generate realistic persona responses using Semantic Similarity Rating.

    This class converts free-text LLM responses into probability distributions
    across Likert scales, producing more realistic response patterns than
    direct numerical elicitation.

    Attributes
    ----------
    rater : ResponseRater
        The underlying SSR rater instance
    reference_config : Dict
        Loaded reference scale configurations
    available_scales : List[str]
        List of available scale IDs

    Examples
    --------
    >>> generator = SSRResponseGenerator("path/to/response_scales.yaml")
    >>> persona = {"age": 25, "experience": "beginner"}
    >>> response = generator.generate_persona_response(
    ...     persona_config=persona,
    ...     stimulus="Complete this vocabulary lesson",
    ...     scale_id="engagement"
    ... )
    >>> print(f"Expected value: {response['expected_value']:.2f}/5")
    """

    def __init__(
        self,
        reference_config_path: Union[str, Path],
        model_name: str = "all-MiniLM-L6-v2",
        device: Optional[str] = None
    ):
        """
        Initialize with reference statements from YAML config.

        Parameters
        ----------
        reference_config_path : str or Path
            Path to YAML file containing reference scale definitions
        model_name : str, optional
            SentenceTransformer model to use, by default "all-MiniLM-L6-v2"
        device : str, optional
            Device to run the model on ('cpu', 'cuda', etc.), by default None (auto-detect)
        """
        self.reference_config_path = Path(reference_config_path)
        self.reference_config = self._load_reference_config()

        # Build polars DataFrame for ResponseRater
        df_refs = self._build_reference_dataframe()

        # Initialize ResponseRater in text mode
        self.rater = ResponseRater(
            df_refs,
            model_name=model_name,
            device=device
        )

        self.available_scales = self.rater.available_reference_sets

    def _load_reference_config(self) -> Dict:
        """Load reference scale configurations from YAML file."""
        if not self.reference_config_path.exists():
            raise FileNotFoundError(
                f"Reference config not found: {self.reference_config_path}"
            )

        with open(self.reference_config_path, 'r') as f:
            config = yaml.safe_load(f)

        if not config:
            raise ValueError(f"Empty config file: {self.reference_config_path}")

        return config

    def _build_reference_dataframe(self) -> po.DataFrame:
        """
        Build polars DataFrame from reference config.

        Returns
        -------
        po.DataFrame
            DataFrame with columns: id, int_response, sentence
        """
        rows = []

        for scale_name, scale_config in self.reference_config.items():
            scale_id = scale_config.get('id', scale_name)
            scale_points = scale_config.get('scale_points', {})

            if not scale_points:
                raise ValueError(f"No scale_points defined for scale: {scale_name}")

            # Validate we have 1-5 scale points
            expected_points = set(range(1, 6))
            actual_points = set(int(k) for k in scale_points.keys())

            if actual_points != expected_points:
                raise ValueError(
                    f"Scale '{scale_name}' must have exactly points 1-5. "
                    f"Found: {sorted(actual_points)}"
                )

            # Build rows for this scale
            for point_num, point_config in scale_points.items():
                statement = point_config.get('statement')
                if not statement:
                    raise ValueError(
                        f"No statement defined for {scale_name} point {point_num}"
                    )

                rows.append({
                    'id': scale_id,
                    'int_response': int(point_num),
                    'sentence': statement
                })

        return po.DataFrame(rows)

    def generate_persona_response(
        self,
        persona_config: Dict,
        stimulus: str,
        scale_id: str,
        llm_response: str,
        temperature: float = 1.0,
        epsilon: float = 0.0
    ) -> Dict:
        """
        Generate response PMF for a persona given an LLM's text response.

        This method takes a free-text LLM response and converts it to a
        probability distribution across the specified Likert scale using
        semantic similarity to reference statements.

        Parameters
        ----------
        persona_config : Dict
            Persona configuration (demographics, attributes, etc.)
        stimulus : str
            The stimulus shown to the persona (for context/logging)
        scale_id : str
            ID of the scale to use (must match a scale in reference config)
        llm_response : str
            The free-text response from the LLM
        temperature : float, optional
            Temperature for PMF scaling (lower = sharper), by default 1.0
        epsilon : float, optional
            Regularization parameter, by default 0.0

        Returns
        -------
        Dict
            Dictionary containing:
            - text_response: Original LLM response
            - pmf: Probability distribution across scale (list of 5 floats)
            - expected_value: Mean of distribution (float)
            - most_likely_rating: Mode of distribution (int 1-5)
            - stimulus: The original stimulus
            - scale_id: The scale used
            - persona_summary: Brief persona description

        Raises
        ------
        ValueError
            If scale_id not found in available scales

        Examples
        --------
        >>> response = generator.generate_persona_response(
        ...     persona_config={"age": 25, "level": "beginner"},
        ...     stimulus="Rate this learning content",
        ...     scale_id="engagement",
        ...     llm_response="This looks interesting and I want to try it"
        ... )
        """
        if scale_id not in self.available_scales:
            raise ValueError(
                f"Scale '{scale_id}' not found. Available: {self.available_scales}"
            )

        # Convert to PMF using SSR
        pmf = self.rater.get_response_pmfs(
            reference_set_id=scale_id,
            llm_responses=[llm_response],
            temperature=temperature,
            epsilon=epsilon
        )[0]  # Get first (only) response

        # Calculate expected value (mean)
        scale_points = np.arange(1, 6)
        expected_value = np.dot(pmf, scale_points)

        # Most likely rating (mode)
        most_likely_rating = int(np.argmax(pmf) + 1)

        return {
            "text_response": llm_response,
            "pmf": pmf.tolist(),
            "expected_value": float(expected_value),
            "most_likely_rating": most_likely_rating,
            "stimulus": stimulus,
            "scale_id": scale_id,
            "persona_summary": self._summarize_persona(persona_config)
        }

    def generate_journey_responses(
        self,
        persona_config: Dict,
        journey_stimuli: List[str],
        llm_responses: List[str],
        scale_id: str,
        temperature: float = 1.0
    ) -> List[Dict]:
        """
        Generate responses across a journey with multiple touchpoints.

        Parameters
        ----------
        persona_config : Dict
            Persona configuration
        journey_stimuli : List[str]
            List of stimuli at each touchpoint
        llm_responses : List[str]
            List of LLM free-text responses (same length as stimuli)
        scale_id : str
            Scale to use for all responses
        temperature : float, optional
            Temperature for PMF scaling, by default 1.0

        Returns
        -------
        List[Dict]
            List of response dictionaries (one per touchpoint)

        Raises
        ------
        ValueError
            If lengths of stimuli and responses don't match
        """
        if len(journey_stimuli) != len(llm_responses):
            raise ValueError(
                f"Mismatch: {len(journey_stimuli)} stimuli but "
                f"{len(llm_responses)} responses"
            )

        return [
            self.generate_persona_response(
                persona_config=persona_config,
                stimulus=stimulus,
                scale_id=scale_id,
                llm_response=response,
                temperature=temperature
            )
            for stimulus, response in zip(journey_stimuli, llm_responses)
        ]

    def get_survey_aggregate(
        self,
        response_pmfs: List[np.ndarray]
    ) -> Dict:
        """
        Aggregate multiple response PMFs into survey-level statistics.

        Parameters
        ----------
        response_pmfs : List[np.ndarray]
            List of PMF arrays

        Returns
        -------
        Dict
            Survey-level statistics including aggregate PMF and expected value
        """
        pmfs_array = np.array(response_pmfs)
        aggregate_pmf = self.rater.get_survey_response_pmf(pmfs_array)

        scale_points = np.arange(1, 6)
        expected_value = np.dot(aggregate_pmf, scale_points)

        return {
            "aggregate_pmf": aggregate_pmf.tolist(),
            "aggregate_expected_value": float(expected_value),
            "n_responses": len(response_pmfs),
            "individual_expected_values": [
                float(np.dot(pmf, scale_points)) for pmf in response_pmfs
            ]
        }

    def _summarize_persona(self, persona_config: Dict) -> str:
        """Create a brief summary string from persona config."""
        key_attrs = ['age', 'experience', 'level', 'role', 'goal']
        parts = []

        for attr in key_attrs:
            if attr in persona_config:
                parts.append(f"{attr}={persona_config[attr]}")

        return ", ".join(parts) if parts else "persona"

    def get_scale_info(self, scale_id: str) -> Dict:
        """
        Get information about a specific scale.

        Parameters
        ----------
        scale_id : str
            Scale ID to query

        Returns
        -------
        Dict
            Scale configuration and reference statements
        """
        if scale_id not in self.available_scales:
            raise ValueError(
                f"Scale '{scale_id}' not found. Available: {self.available_scales}"
            )

        # Find the scale in config
        scale_config = None
        for scale_name, config in self.reference_config.items():
            if config.get('id', scale_name) == scale_id:
                scale_config = config
                break

        return {
            "scale_id": scale_id,
            "description": scale_config.get('description', ''),
            "reference_sentences": self.rater.get_reference_sentences(scale_id),
            "scale_points": scale_config.get('scale_points', {})
        }

    def __repr__(self) -> str:
        return (
            f"SSRResponseGenerator("
            f"scales={len(self.available_scales)}, "
            f"model={self.rater.model_info})"
        )
