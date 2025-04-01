# Using the Engagement Pattern System

This document provides instructions on how to use the example component that demonstrates the engagement pattern system.

## Setup

1. Install the project dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Navigate to the example component in your application.

## Understanding the Example

The example in `example_usage.tsx` demonstrates how to use the Engagement Pattern System with these key features:

### 1. User Persona Customization

- You can switch between different persona types to see how content adapts:
  - **Health-Aware Avoiders**: Cautious users with health anxiety
  - **Structured System-Seekers**: Analytical users who prefer systematic processes
  - **Balanced Life Integrators**: Users with a holistic approach to health
  - **Healthcare Professionals**: Users with medical knowledge
  - **Overlooked Risk Group**: Users with lower healthcare engagement

### 2. Content Type Selection

- The system offers three levels of content depth:
  - **Essential**: Core information that should be immediately visible
  - **Extended**: Additional context and details
  - **Comprehensive**: Deep dive content with detailed information

### 3. Dynamic Content Adaptation

The example shows how:
- Content is automatically enhanced with value articulation (why it matters)
- Emotional scaffolding adjusts to provide appropriate support
- Content presentation adapts to the user's persona

### 4. Engagement Tracking

- When you click the completion button, metrics are collected and displayed including:
  - Value articulation effectiveness
  - Emotional scaffolding appropriateness
  - Progressive disclosure optimization
  - Persona alignment score

## Customizing for Your Application

To integrate this into your own components:

1. Import the necessary components:
   ```tsx
   import { JourneyStepComponent } from './src/engagement/components/journey_step';
   import { User, JourneyStep } from './src/engagement/types';
   ```

2. Create user and step objects:
   ```tsx
   const user: User = {
     id: "user-id",
     persona: "persona-type",
     email: "user@example.com",
     createdAt: new Date().toISOString(),
     updatedAt: new Date().toISOString()
   };

   const step: JourneyStep = {
     id: "step-id",
     type: "essential", // or "extended", "comprehensive"
     content: "Your content here...",
     visibility: "visible"
   };
   ```

3. Use the component:
   ```tsx
   <JourneyStepComponent 
     step={step}
     user={user}
     onComplete={(stepId, metrics) => {
       // Handle completion
     }}
   />
   ```

4. Access lower-level pattern functionality if needed:
   ```tsx
   import { useEngagementPatterns } from './src/engagement/use_engagement_patterns';

   function YourComponent() {
     const { enhanceJourneyStep } = useEngagementPatterns();
     
     // Use the patterns directly
     const result = await enhanceJourneyStep(step, user);
     
     // ... rest of your component
   }
   ```

## Best Practices

1. **Progressive Content Loading**: Start with essential content and progressively reveal more.
2. **Persona-Aware Design**: Consider different user types when crafting content.
3. **Emotional Intelligence**: Include supportive messaging appropriate to the context.
4. **Value Communication**: Always articulate why a step matters to the user.
5. **Metrics Analysis**: Use the pattern metrics to refine your content strategy.