## [1.0.9] - 2026/02/22
### Legal Pages

### Added
- Terms of Use and Privacy Policy pages.
- LICENSE file.

### Changed
- Footer now links to Terms and Privacy.

## [1.0.7] - 2026/02/22
### Rental Emoji Selection

### Added
- **Rental form**:
  - Emoji dropdown to select the dumpster icon explicitly.

### Changed
- **Rental emoji logic**:
  - Honors the selected emoji when present, otherwise falls back to title prefix.
- **Dashboard note**:
  - Updated guidance to mention the new dropdown.

## [1.0.8] - 2026/02/22
### Rental Emoji Cleanup

### Changed
- **Rental emoji logic**:
  - Removed title-based emoji selection; dropdown is now the only source.
- **Rental form**:
  - Emoji selection is always required (defaults to A).
- **Dashboard note**:
  - Simplified guidance to match the new behavior.

## [1.0.6] - 2026/02/22
### Dashboard Updates

## [1.0.5] - 2026/02/22
### Mobile-Friendly UI Cleanup

### Added
- **Global styling**:
  - Shared color/spacing variables and base styles.
  - Viewport meta tag and `<main>` wrapper for layout consistency.

### Changed
- **Navigation**:
  - Responsive spacing and button styling for mobile.
- **Landing, Articles, Videos, Dashboard**:
  - Updated layouts and card styling to match the rentals design language.
- **Footer**:
  - Removed inline styles in favor of stylesheet rules.

## [1.0.4] - 2026/02/22
### Rentals Calendar Refresh

### Added
- **Dumpster icons**:
  - `DUMPSTER_ICONS` YAML mapping and initializer.
  - Emoji cycling in the rentals legend (CSS-only).
  - Phone link in the legend for quick availability calls.

### Changed
- **Rentals calendar UI**:
  - Reworked layout, copy, and styling for clarity and readability.
  - Calendar cells now render dumpster emojis instead of colored squares.
- **Rental model**:
  - Emoji selection now pulls from `DUMPSTER_ICONS` with safe fallbacks.

## [1.0.3] - 2026/02/22
### Runtime Updates

### Changed
- **Ruby**: Updated to 4.0.1 (pinned in `.ruby-version`, `Gemfile`, and `Dockerfile`).
- **Rails**: Updated to 8.1.2 (pinned in `Gemfile` and `Gemfile.lock`).
- **README**: Updated version references.

## [1.0.2] - 2025/04/02
### Dashboard Enhancements & Calendar Context

### Added
- **Navigation**:
  - Contact phone number listed under logo

## [1.0.1] - 2025/04/02
### Dashboard Enhancements & Calendar Context

### Added
- **Navigation**:
  - "Edit Profile" link added to nav for signed-in users.
- **Dashboard**:
  - Ability to create new `Article` and `Video` entries directly from the dashboard.

### Changed
- **Rental Calendar Context**:
  - `rentals/index.html.erb` now includes a short explanation of what the calendar is displaying.
- **Scaffold Navigation**:
  - All `edit` and `show` pages now include a link back to the dashboard for smoother admin workflow.

### Removed
- **`articles/index.html.erb`**:
  - Removed the "Show this article" link to simplify the index view.

### Notes
- Enhances UX for admin users managing content.
- Provides clearer calendar context for rentals.

## [1.0.0] - 2025/04/02

### Changed
- **Footer**: Centered for better alignment.
- **App Name**: Updated to reflect new branding.
- **Navigation**: Removed unnecessary items for a cleaner layout.

## [0.1.10] - 2025/04/02
### Finalizing before release 

### Changed  
- **`index.html.erb`**:  
  - Removed unnecessary bloat for a cleaner, more efficient layout.  
- **`application.scss`**:  
  - Set default font to Arial sitewide for a consistent look.  
- **`calendar/show.html.erb`**:  
  - Fixed calendar display issue by adjusting absolute positioning (thanks to ChatGPT!).  
  - Added actual date display for each day on the calendar.  

### Added  
- Authentication for editing actions (to restrict unauthorized access).

### Notes  
- Improved calendar layout and functionality.  
- Streamlined the homepage for better performance.  
- Enhanced security with authentication for edits.


## [0.1.9] - 2025/04/02  
### Dashboard Updates  

### Changed  
- **`dashboard/index.html.erb`**:  
  - Displayed basic info for each object in the database (title only) with links to edit.
  - Other changes made to related controllers for auth.

## [0.1.8] - 2025/04/02
### Pre-Release

### Added
- Videos section created and styled.

### Changed
- Imported `articles.scss` into **`application.scss`** (oops).

## [0.1.7] - 2025/04/02
### Pre-Release

### Changed
- Imported `simple-calendar` into **`application.scss`**.
- Added emoji support between **`models/rental.rb`** and **`rentals/index.html.erb`**.

## [0.1.6] - 2025/04/01
### Pre-Release

### Added
- **`console.rb`** added to `.gitignore`.
- **`article.scss`** stylesheet added.

### Changed
- Updated **`article`**:
  - Display images on the article show page.
  - Featured articles section added.
  - Articles cannot be edited without authentication.
- Updated **`nav`**:
  - Changed `logout` to a button to prevent errors.

## [0.1.5] - 2025/04/01
### Pre-Release

### Changed
- Uncommented `user_signed_in?` from navigation.
- Added calendar to **`rentals/index.html.erb`**.
- Applied stylization throughout using `sassc` gem.
  - Split styles into individual sections (e.g., nav, landing, etc.).
- Added logo and landing images (1-3).
- Updated homepage to display landing information.

## [0.1.4] - 2025/04/01
### Pre-Release

### Added
- Home page content added.
- Dashboard updated.
- dashboard_controller referencing current_user for the page as @user

### Removed
- confirmable from user model

## [0.1.3] - 2025/04/01
### Pre-Release

### Added
- Basic layout established with navigation and footer.

### Changed
- Commented out `sign_in` related sections for now in the navigation.

## [0.1.2] - 2025/04/01
### Pre-Release  

### Added  
- **`dashboard_controller`**:  
  - Authenticates user and ensures approval before access.  
- **`home_controller`**:  
  - Serves as the public landing page.  

### Changed  
- **Routes**:  
  - Set root path to `home#index`.  

## [0.1.1] - 2025/04/01
### Pre-Release

### Added
- Generated scaffolds for:
  - **`landing_card`**: `title`, `description`, `image`
  - **`pricing_card`**: `title`, `description`, `image`
  - **`article`**: `title`, `description`, `body`, `image`
  - **`rental`**: `title`, `address`, `start_time`, `end_time`
  - **`video`**: `title`, `description`, `youtube_id`

## [0.1.0] - 2025/04/01
### Pre-Release

### Added
- Implemented `simple_calendar` and `devise` gems.
- Created `User` model with Devise integration.
  - User approval required for access.
