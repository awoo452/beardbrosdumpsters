# Beard Bros Dumpsters

Beard Bros Dumpsters is a Rails 7 app for a local dumpster rental business. It provides a public marketing site plus a lightweight admin dashboard for managing landing cards, articles, rentals, pricing cards, and videos.

**Features**
- Public pages: Home, Articles, Rentals (calendar), Videos.
- Admin dashboard (approved users only) with quick links to edit content.
- Rentals calendar uses `simple_calendar` and visual blocks to indicate booked dumpsters.
- Devise authentication with manual approval gating.

**Tech Stack**
- Ruby 4.0.1
- Rails 8.1.2
- PostgreSQL
- Devise
- Simple Calendar
- SassC

**Documentation**
- Home page pulls the latest three `LandingCard` records.
- Articles page lists full articles (title, description, body, optional image).
- Rentals page shows a month view calendar. Each rental paints a colored block for every day between `start_time` and `end_time`.
- The app assumes three dumpsters total. If a date shows fewer than three blocks, there is likely availability (the UI still advises customers to call to confirm).
- Videos page embeds YouTube videos using the `youtube_id` field. Add `?autoplay=1` to the URL to auto-play the embeds.
- Pricing cards exist but are not linked in the main nav. They can be visited at `/pricing_cards`.
- Only signed-in users can create/edit content. The dashboard link appears only for approved users.

**Admin Workflow**
- Sign up via Devise.
- Approve the user in the Rails console:

```ruby
user = User.find_by(email: "you@example.com")
user.update!(approved: true)
```

- Visit `/dashboard` to access links for managing content.

**Local Development**
- Install Ruby 4.0.1 and PostgreSQL.
- Install gems:

```bash
bundle install
```

- Create and migrate the database:

```bash
bin/rails db:create db:migrate
```

- Start the server:

```bash
bin/rails server
```

**Images**
- Image fields store a filename (for example `landing1.png`).
- Place images in `app/assets/images` and reference the filename in records.

**Sample Landing Cards**

```ruby
LandingCard.create!([
  {
    title: "Dumpster Rentals with Delivery Service",
    description: "Fast and affordable dumpster delivery options, servicing the greater Pennsylvania area. We drop it off, you fill it up with junk, we pick it up. Pretty easy!",
    image: "landing1.png"
  },
  {
    title: "Putting Your Junk in Our Trunk Since 2023",
    description: "If the junk is there, we can make it disappear. Give us a shout and throw it out today!",
    image: "landing2.png"
  },
  {
    title: "You Call, We Haul",
    description: "Contact us today to schedule your next delivery. Head on over to the Articles section to see our latest new & events, or the Rentals page if you want to see our general dumpster availability.",
    image: "landing3.png"
  }
])
```

**Notes**
- Calendar rendering logic lives in `app/views/rentals/index.html.erb` and uses the rental title to pick a colored block.
- No UI exists for user approval, so approvals are handled through the console.
