# Beard Bros Dumpsters

Beard Bros Dumpsters is a Rails 7 app for a local dumpster rental business. It provides a public marketing site plus a lightweight admin dashboard for managing landing cards, articles, rentals, pricing cards, and videos.

## Features

- Public pages: Home, Articles, Rentals (calendar), Videos.
- Admin dashboard (approved users only) with quick links to edit content.
- Rentals calendar uses `simple_calendar` and visual blocks to indicate booked dumpsters.
- Devise authentication with manual approval gating.

### Documentation

The Home page displays the latest three `LandingCard` records.
The Articles page lists full articles (title, description, body, and optional image).
The Rentals page shows a month view calendar. Each rental paints a colored block for each day between `start_time` and `end_time`.
The app assumes three dumpsters total. If a date has fewer than three blocks, there is likely availability (UI still advises customers to call to confirm).
The Videos page embeds YouTube videos using the `youtube_id` field. Add `?autoplay=1` to the URL to auto-play embeds.
Only signed-in, approved users can create/edit content. The dashboard link appears only for approved users.

### Admin Workflow

1. Sign up via Devise.
2. Approve the user in the Rails console:
   ```ruby
   user = User.find_by(email: "you@example.com")
   user.update!(approved: true)
   ```
3. Visit `/dashboard` to access links for managing content.

### Images

- Image fields store a filename (for example, `landing1.png`).
- Place images in `app/assets/images` and reference the filename in records.

### Sample Landing Cards

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
    description: "Contact us today to schedule your next delivery. Head on over to the Articles section to see our latest news & events, or the Rentals page if you want to see our general dumpster availability.",
    image: "landing3.png"
  }
])
```

### Notes

- Calendar rendering logic lives in `app/views/rentals/index.html.erb` and uses the rental title to pick a colored block.
- No UI exists for user approval; approvals are handled in the console.

## Setup

Prereqs: Ruby 4.0.2, Rails 8.1.2, PostgreSQL, Devise, Simple Calendar, SassC.

1. `bundle install`
2. `bin/rails db:create db:migrate`

## Run

1. `bin/rails server`

## Tests

1. `bin/rails test`
2. `bin/rails test:system`

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for notable changes.
