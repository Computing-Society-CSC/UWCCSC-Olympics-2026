# UWCCSC Olympics 2026 - Development Plan

## Project Overview
**Team Structure**: 
- **Frontend Developer**: Responsible for templates, CSS, JavaScript, user interface
- **Backend Developer**: Responsible for database models, routes, authentication, business logic

## Week-by-Week Development Timeline

### Week 1: Project Setup and Foundation
- **先提前把工分好**
- **在抖音上找一下cline怎么用，一定要学会用ai去写代码改代码，效率会高很多，但是也要学会能发现ai的错误并及时纠正，同时写清晰明了的prompt也很重要**

**Frontend Tasks**:
- Set up project directory structure
- Create base template (`base.html`) with navigation, footer, and responsive layout
- Create basic CSS structure with school color scheme
- Design wireframes for all major pages

**Backend Tasks**:
- Set up Flask application structure
- Create `models.py` with initial database models **这个可以参照去年的models.py文件**
- Set up SQLite database configuration
- Create `config.py` with application settings
- Implement basic authentication system (secret key based)
- Create `run.py` entry point

**Collaboration**:
- Agree on template inheritance structure
- Set up Git repository with branching strategy **这里你们可以讨论一下，同时自己去做做research该怎么样合理使用dev和main两个branch**

### Week 2: Core Public Viewing Features

**Frontend Tasks**:
- Create `homepage.html` with match listings and status indicators
- Design `match_view.html` for detailed match information
- Implement `houses_status.html` with real-time rankings display
  - **Note**: Implement logic to hide rankings on Day 3 (surprise element)
- Create `timetable.html` with organized schedule by date **这个可以等后面timetable出来了再做**
- Design `about.html` with Olympics information
- Implement responsive design for all public pages

**Backend Tasks**:
- Create routes for public pages in `routes.py`:
  - `/` - Homepage
  - `/match/<int:match_id>` - Match details
  - `/houses` - House rankings (with Day 3 hiding logic) **为了预留一些惊喜，olympics core team希望我们只给公众展示前两天的排名，详情见Website_Functions.md**
  - `/timetable` - Schedule
  - `/about` - About page
- Implement database queries for match listings
- Create house ranking calculation logic

### Week 3: Management System & Authentication

**Frontend Tasks**:
- Design `management_home.html` dashboard
- Create `management_matches.html` for match management
- Implement `management_house_rankings.html` for admin house management
- Design `create_matches.html`, `edit_match.html` forms
- Create `management_upload_scores.html` for score entry
- Implement secret key authentication interface

**Backend Tasks**:
- Implement secret key authentication middleware
- Create management routes in `routes.py`:
  - `/management` - Dashboard
  - `/management/matches` - Match management
  - `/management/matches/create` - Create match
  - `/management/matches/<int:match_id>/edit` - Edit match
  - `/management/matches/<int:match_id>/delete` - Delete match
  - `/management/houses` - House management
  - `/management/scores/upload` - Upload scores
- Create `forms.py` with WTForms for all management forms
- Implement CRUD operations for matches

### Week 4: Tournament Bracket System

**Frontend Tasks**:
- Design tournament bracket visualization component
- Create `match_management.html` for bracket management
- Implement bracket display in `match_view.html`
- Design winner propagation interface
- Create responsive bracket display for mobile and desktop

**Backend Tasks**:
- Implement automatic bracket generation algorithm
- Create bracket data structure in database
- Implement winner propagation logic
- Add tournament round management to models
- Create routes for bracket operations:
  - `/tournament/generate` - Generate brackets
  - `/tournament/advance` - Advance winners
  - `/match/<int:match_id>/winner` - Assign winners

### Week 5: Scoring System & Advanced Features

**Frontend Tasks**:
- Implement real-time update indicators using JavaScript
- Create scoring display with point breakdown
- Design special house multiplier interface
- Implement sportsmanship messages and inclusive language
- Add accessibility features (keyboard navigation, alt text)
- Create congratulatory messages for participants

**Backend Tasks**:
- Implement automatic point calculation:
  - Individual events: 25-20-15 points
  - Team events: 50-45-40 points
  - House events: 75-65-55 points
- Add special house multipliers (B3 Baile, C5 Efie)
- Implement manual winner assignment
- Create real-time update system (WebSocket or polling)
- Add logging and error handling

### Week 6: Integration, Polish & Deployment

**Frontend Tasks**:
- Perform cross-browser testing
- Optimize CSS and JavaScript performance
- Implement subtle animations for enhanced UX
- Ensure WCAG accessibility compliance
- Test responsive design on multiple devices
- Polish visual design and user interactions

**Backend Tasks**:
- Integrate all components and test end-to-end
- Implement database migrations system
- Add input validation and error handling
- Optimize database queries
- Set up production configuration
- Prepare deployment scripts

**Collaboration**:
- Integration testing of all features
- Performance optimization
- Security review
- Deployment to production server
- Documentation finalization

## Key Technical Requirements

### 1. Day 3 Ranking Hiding Logic
- Implement date-based logic to check if current day is Day 3
- If Day 3, display "Rankings hidden until final announcement" message
- Management view still shows actual rankings **这里很重要，第三天一定要能够区分开给公众展示的排名和管理者能够看到的真实排名）
- Use server-side date checking to prevent client-side manipulation

### 2. Real-time Updates
- Visual indicators when scores change
- Automatic page refresh for ranking updates

### 3. Sportsmanship and Inclusivity
- Congratulatory messages for all participants
- Emphasis on participation over winning
- Inclusive language throughout interface
- Celebration of sportsmanship moments

## Risk Mitigation

### Technical Risks:
1. **Database performance**: Implement caching for frequently accessed data
2. **Real-time updates scalability**: Use efficient polling if WebSockets prove complex
3. **Day 3 hiding bypass**: Implement server-side validation, not just client-side
4. **Mobile compatibility**: Extensive testing on various devices

### Project Risks:
1. **Timeline slippage**: Weekly progress reviews and adjust scope if needed
2. **Integration issues**: Daily standups and frequent integration testing
3. **Knowledge gaps**: Pair programming sessions and documentation

## Success Metrics
- Application deployed on time (Week 6)
- All core functions from Website_Functions.md implemented
- Positive user feedback on interface and usability
- No critical bugs in production
- Accessibility requirements met
- Performance: Page load < 2 seconds, database queries < 100ms

## Weekly Review Process
- Monday: Plan week's tasks and assign responsibilities
- Wednesday: Mid-week check-in and problem-solving
- Friday: Demo completed work and review progress
- End of week: Update project plan and adjust as needed

## **一定要多沟通，有什么不懂不确定的一定要及时问问题，这次时间还是挺紧的，希望你们能尽量把这个project做好**
## **一定要做到精益求精，不要糊弄了事，比如前端要是做好了还可以继续给ai喂提示词让他继续优化，让整个界面变得更好看一点**
## **这个文件和Website_Functions.md两个文件都是我用ai写的，在development的过程中随时修改，很灵活的，你们有什么想法想要添加或者删减功能都是可以的**