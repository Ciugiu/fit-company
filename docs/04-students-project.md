# Project

The fitness app is working great and the user base continues to grow.

We now need to start billing users to generate revenue to our nice investors.

Following product marketing analysis, we identified the following features to add to the app:

- Billing service to allow users to pay for premium features
- Here are some premium features (you can implement other features if you want):
  + Premium workout plans: allows users to get 9 exercises per workout
  - Allow users to cancel their subscription
  - Persist exercise reps and weights
  - Announce when user reaches a new milestone (1000 pushups, 10000 steps, 100000 calories, etc.)
  + Allow users to change their WOD (workout of the day)
  - Add notifications to users when their subscription is about to expire

You should add as many features as you can in the project, but add features one by one, the project should be running at all times.

At the beginning you should split the work into two teams, one team will work on the billing service and the other team will work on the premium features implementation.

## Project presentation

You will be presenting your project to the teacher as a group.

Presentation should be split into three parts (10 minutes presentation + 10 minutes questions):

- Implemented features description + flow diagrams
- Demo of the features in action using Bruno/Postman/curl
- Questions and answers: walking through the code (10 minutes)

Each group will present on one member's computer, the project should be set-up correctly and running at the beginning of the presentation. The code should be opened in your IDE.

You will be asked to explain your code and the decisions you made, every student will be asked to answer questions about the project.

There will be a team grade and a personal grade.

## Project submission

You should submit a pull request before the beginning of the presentation to the `event-driven` branch of the upstream repository `wayglem/fit`.

## About the billing service

We won't integrate with any payment provider. You should mock the payment flow making it as realistic as possible.

Start with a simple flow and add more features as you go.
