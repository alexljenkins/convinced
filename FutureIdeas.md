# Develop Plan

## Milestone 1: Website Reconstruction & Enhancement

***GOAL:** Set a solid foundation for the web app, aligning it with modern development practices and preparing for further enhancements in subsequent milestones.*

1. **Website Rebuild:**
    - Refactor existing code to improve efficiency and readability.
    - Replace any deprecated methods with modern alternatives.

2. **Database Redesign:**
    - Change the database from SQLite to PostgreSQL. Design tables to expect lots of different questions, scenarios and interaction types.
    - Ensure data integrity and optimize queries for performance.

3. **Modular Design:**
    - Structure the code to facilitate future development and feature integration.
    - Utilize Next.js or Django for the web framework, and Python with FastAPI for the backend.

4. **Front End Development:**
    - Page 1: Create a single page where users can interact with an alien scenario.
    - Page 2: Allow the user to take the Alien's perspective and vote on convincing responses.

5. **Additional Features:**
    - "Report Response" button: Users can report inappropriate or irrelevant responses on Page 2.
    - User Account Management: Option to register/login for tracking individual scores or responses.
    - Response Categorization: Implement tagging or categorization of responses for analysis.

6. **Testing & Quality Assurance:**
    - Implement unit and integration tests to ensure functionality.
    - Conduct user testing for usability and experience optimization.

7. **Documentation & Compliance:**
    - Ensure that all code is well-documented.
    - Comply with relevant legal regulations and standards.

## Milestone 2: Scenario Expansion & User Engagement

***GOAL:** Milestone 2 focuses on expanding the user experience, adding a storyline to the scenarios, and introducing features that drive user engagement and retention. It builds upon the foundation set in Milestone 1, taking the web app to a more immersive and interactive level.*

1. **Scenario Development:**
    - Create 4 more alien-related scenarios that occur in series.
    - Include diverse interactions such as befriending the alien, teaching, negotiating, etc.
    - Implement failure mechanisms, prompting the user to create an account to retry the level.

2. **Account Creation & Progress Saving:**
    - Integrate Google and email registration for account creation.
    - Implement profile pages for members, including a progress tracking system.
    - Prompt users to unlock the final level by creating an account if they surpass level 4.

3. **Visual Effects & Engagement:**
    - Develop engaging visual effects that resonate with the alien theme.
    - Create interactive background scenes with a cohesive art style.
    - Ensure that visual elements enhance user experience without distracting from the core gameplay.

4. **Testing & Quality Assurance:**
    - Conduct extensive testing to ensure that all scenarios function properly.
    - Evaluate user experience with visual effects and the account creation flow.
    - Verify that account creation and progress saving mechanisms are secure and functional.

5. **Documentation:**
    - Update existing documentation to include details of the new scenarios, account management features, and visual effects.
    - Ensure compliance with privacy regulations regarding user data handling.

## Milestone 3: Gamification & User Engagement Enhancement

***GOAL:** Boost user engagement by introducing competitive elements and rewards. By offering tangible goals and incentives, it encourages continuous participation and fosters a community atmosphere. It's an essential step in prepping the app for future expansion and potential monetization.*

1. **Rankings and Leaderboards:**
    - Implement 2 scoring systems:
        - 1 based user performance, voting accuracy, ranking etc.
        - 1 based on contribution, time, effort and engagement.
    - Create leaderboards for various categories (e.g., weekly, all-time, friends).
    - Display rankings and allow users to compare their performance with others.

2. **Points & Rewards:**
    - Introduce a point system to reward user engagement, such as reviewing, voting, and attempting the scenarios.
    - Provide special cosmetics and badges for achieving certain milestones:
    - Reviewing and marking 10, 20, 50, 100, 500 other works.
    - Ranking in the top 1% of submissions, both user and AI-voted.
    - Completing all levels without failure.
    - Inviting friends to play.
    - Participating in special events or challenges.

3. **User Experience Enhancements:**
    - Add a quest log or achievements page to break down rewards and show progress in the scoring and rewards system. Including what other tasks they could explore.
    - Implement a customization feature, allowing users to personalize their profile or in-game appearance.

4. **Testing & Quality Assurance:**
    - Thoroughly test the new gamification features, ensuring smooth integration.
    - Validate that rewards are assigned correctly (for the current state of things) and that the leaderboards are accurate.

5. **Documentation:**
    - Provide detailed documentation for the new scoring system, points, and rewards.
    - Update user guides or FAQs to include the latest features.

## Milestone 4: Integration of Advanced Analytics, Admin and Business Features

***GOAL:** Focus on enhancing the app's educational impact, personalizing the experience, fostering community, and ensuring security and accessibility. This phase can significantly elevate the app as an educational tool, appealing to schools, educators, students, and parents alike. It's about creating an ecosystem that supports learning, engagement, and collaboration in an enjoyable and safe environment.*

1. **Advanced Analytics & Reporting:**
    - Admin Accounts and Management: SSO and Admin pannel to manage a licence across a business/school.
    - Student Progress Tracking: Provide insights for teachers and parents on student progression, strengths, and areas for improvement.
    - Classroom Analytics: Enable educators to understand class performance, engagement, and areas where additional support may be needed.
    - Personalized Feedback: Generate specific feedback for students based on their performance, guiding them towards improvement.

2. **Customization & Accessibility:**
    - Adaptive Learning Paths: Create tailored scenarios that adapt to individual student needs and learning paces.
    - Accessibility Features: Ensure the app is inclusive and usable by all students, including those with disabilities. Provide alternative text, voice-over features, etc.
    - Language Options: Offer multiple language support for diverse student populations.

3. **Community Engagement & Collaboration:**
    - Teacher Collaboration Tools: Allow teachers to share resources, create custom scenarios, and collaborate on class activities.
    - Parent Engagement: Offer features that allow parents to be involved in their children’s learning, such as notifications, summaries, or collaborative activities.
    - Student Peer Interaction: Encourage students to work together, compete, or provide peer feedback within a safe and moderated environment.

4. **Content Expansion & Partnerships:**
    - Curriculum Alignment: Ensure scenarios align with national or regional educational standards and subjects.
    - Educational Partnerships: Collaborate with schools, educational organizations, or content providers to enrich the app's educational value.
    - Seasonal or Themed Content: Regularly update with new, exciting content to keep students engaged.

5. **Security & Compliance:**
    - Data Privacy & Security: Implement robust security measures to protect student data and comply with relevant regulations.
    - Teacher & Parent Controls: Provide necessary controls to ensure age-appropriate content and interactions.

6. **Marketing & Outreach:**
    - School Engagement Programs: Develop programs to encourage adoption in schools, offering training, support, and customization.
    - Community Outreach: Engage with local communities and educational authorities to promote the app as a valuable educational tool.

## Scenario Ideas

#### Idea 2: Crisis Negotiation

- Level 1: Talk a friend through a minor personal crisis.
- Level 2: Mediate a heated argument between coworkers.
- Level 3: Negotiate with a demanding client.
- Level 4: Handle a community dispute or protest.

#### Idea 3: Adventure Storytelling

- Level 1: Describe an adventurous day at a local park.
- Level 2: Tell the tale of a thrilling mountain climb.
- Level 3: Narrate a perilous jungle expedition.
- Level 4: Convey an epic space exploration story.

#### Idea 4: Building Trust with an Alien Civilization

- Level 1: Establish first contact and common ground.
- Level 2: Share cultural values and beliefs.
- Level 3: Create a mutual agreement or treaty.
- Level 4: Collaborate on a joint mission or project.

#### Idea 5: Political Campaign

- Level 1: Explain your position on a local issue.
- Level 2: Persuade voters in a town hall meeting.
- Level 3: Debate with other candidates.
- Level 4: Deliver a victory speech.

#### Idea 6: Emergency Response Team

- Level 1: Guide a lost person back to safety.
- Level 2: Coordinate a rescue operation during a flood.
- Level 3: Command a team in a wildfire containment.
- Level 4: Lead a response to a major natural disaster.

#### Idea 7: Movie Directing

- Level 1: Pitch a movie idea to producers.
- Level 2: Direct a complex scene with multiple actors.
- Level 3: Handle media interviews and promotion.
- Level 4: Give an acceptance speech at an awards ceremony.

#### Idea 8: Medical Consultation

- Level 1: Explain a diagnosis to a patient.
- Level 2: Comfort a worried family member.
- Level 3: Discuss a complex treatment plan.
- Level 4: Lead a team through a surgical procedure.

#### Idea 9: Corporate Leadership

- Level 1: Inspire a team for a new project.
- Level 2: Navigate company politics and conflicts.
- Level 3: Present to the board of directors.
- Level 4: Announce a major company change.

#### Idea 10: Space Exploration Training

- Level 1: Instruct a class of aspiring astronauts.
- Level 2: Guide a simulated space mission.
- Level 3: Command a real space mission to the moon.
- Level 4: Lead humanity's first mission to Mars.

#### Idea 11: School Project Teamwork

- Level 1: Plan a group project with classmates.
- Level 2: Resolve a disagreement within the team.
- Level 3: Present the project to the class.
- Level 4: Reflect on what went well and what could be improved.

#### Idea 12: Environmental Awareness Campaign

- Level 1: Create a poster to promote recycling.
- Level 2: Organize a school clean-up day.
- Level 3: Give a speech about reducing waste.
- Level 4: Lead a community awareness event.

#### Idea 13: Animal Care Adventure

- Level 1: Convince parents to adopt a pet.
- Level 2: Train the pet using positive reinforcement.
- Level 3: Help a lost animal find its home.
- Level 4: Organize a pet awareness fair at school.

#### Idea 14: Time Travel History Lessons

- Level 1: Interview a historical figure from ancient times.
- Level 2: Witness and report on a significant historical event.
- Level 3: Debate historical changes and their impact.
- Level 4: Create a multimedia presentation on a historical era.

#### Idea 15: Science Fair Invention

- Level 1: Brainstorm an innovative science project.
- Level 2: Explain the invention to friends.
- Level 3: Present the invention at a science fair.
- Level 4: Respond to judges’ questions and critiques.

#### Idea 16: Literary Exploration

- Level 1: Describe a favorite book character.
- Level 2: Rewrite a scene from a book in your own words.
- Level 3: Write a letter to an author.
- Level 4: Create a short story in a favorite literary style.

#### Idea 17: Peer Mediation

- Level 1: Help two friends solve a small misunderstanding.
- Level 2: Mediate a conflict in a school club.
- Level 3: Facilitate a solution to a school-wide issue.
- Level 4: Teach others about effective mediation.

#### Idea 18: Artistic Expression Journey

- Level 1: Draw and explain a personal symbol.
- Level 2: Collaborate on a class mural.
- Level 3: Organize an art show.
- Level 4: Reflect on the power of art in communication.

#### Idea 19: Digital Citizenship

- Level 1: Understand and practice internet safety.
- Level 2: Explore the ethics of online behavior.
- Level 3: Create a digital project that benefits the community.
- Level 4: Lead an online safety workshop.

#### Idea 20: Exploring Careers

- Level 1: Interview a family member about their job.
- Level 2: Research and present on a dream career.
- Level 3: Simulate a day in the life of a chosen profession.
- Level 4: Reflect on personal skills and future aspirations.
