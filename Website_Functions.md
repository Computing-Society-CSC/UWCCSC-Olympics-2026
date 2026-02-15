## **CORE WEBSITE FUNCTIONS**

### **1. Public Viewing Functions (No Authentication Required)**
- **Home Page**: Displays all matches/events with their status (Scheduled, In Progress, Completed)
- **Match Details View**: Shows detailed information for individual matches including:
  - Match name, description, start/end times
  - Tournament bracket visualization with rounds
  - Rankings (1st, 2nd, 3rd place winners)
- **House Rankings**: Real-time display of house standings with points and colors
  - **Note**: The Olympics lasts for three days. To create suspense and surprise, house rankings will only be displayed publicly during the first two days. On the third day, rankings will be hidden until the final announcement.
- **Timetable**: Organized schedule of matches grouped by date
- **About Page**: General information about the Olympics

### **2. Management Functions (Requires Secret Key Authentication)**
- **Management Dashboard**: Central hub for all administrative functions
- **House Management**:
  - View real-time house rankings
  - Manually update house points
- **Match Management**:
  - Create new matches/events with name, times, description, category
  - Edit existing match details
  - Delete matches
  - View all matches with status filtering
  - Match status management (Scheduled → In Progress → Completed)

### **3. Tournament Bracket System**
- **Automatic Bracket Generation**: Creates the matchup information automatically by entering a ordered-list of all the houses competing (no need to manually enter the matchup for each game)
- **Score Upload**: Update scores for individual matches
- **Winner Propagation**: Automatically advances winners to next rounds

### **4. Scoring and Ranking System**
- **Automatic Point Calculation**: Different point values for: (Currently there is a bug in the automatic point calculation, but the issue will be addressed this year)
  - Individual events: 25-20-15 points for 1st-2nd-3rd
  - Team events: 50-45-40 points for 1st-2nd-3rd  
  - House events: 75-65-55 points for 1st-2nd-3rd
- **Special House Multipliers**: B3 Baile and C5 Efie houses have adjusted scoring
- **Manual Winner Assignment**: Assign 1st, 2nd, 3rd place winners for matches

### **5. Frontend Design and User Experience**
- **Sportsmanship Emphasis**: The interface should celebrate participation and effort, not just winning. Include congratulatory messages for all participants and highlight sportsmanship moments.
- **Inclusivity and Accessibility**: 
  - Ensure color contrast meets WCAG standards for users with visual impairments
  - Use inclusive language throughout the interface
  - Support keyboard navigation for users who cannot use a mouse
  - Provide alternative text for all images and visual elements
- **Engaging Visual Design**:
  - Use the school's color scheme and branding consistently
  - Implement responsive design for mobile, tablet, and desktop viewing
  - Include subtle animations to enhance user experience without being distracting
  - Display house colors prominently to foster house pride and identity
- **Real-time Updates**: Provide clear visual indicators when scores or rankings are updated to keep users informed
