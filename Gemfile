source "https://rubygems.org"

ruby "4.0.2"

# Use edge Rails instead: gem "rails", github: "rails/rails", branch: "main"
gem "rails", "~> 8.1.2"

# The original asset pipeline for Rails. See: https://github.com/rails/sprockets-rails
gem "sprockets-rails"

# Use PostgreSQL as the database for Active Record
gem "pg", "~> 1.1"

# Use the Puma web server. See: https://github.com/puma/puma
gem "puma", ">= 5.0"

# Use JavaScript with ESM import maps. See: https://github.com/rails/importmap-rails
gem "importmap-rails"

# Hotwire's SPA-like page accelerator. See: https://turbo.hotwired.dev
gem "turbo-rails"

# Hotwire's modest JavaScript framework. See: https://stimulus.hotwired.dev
gem "stimulus-rails"

# Build JSON APIs with ease. See: https://github.com/rails/jbuilder
gem "jbuilder"

# SassC integration for Rails
gem "sassc-rails", "~> 2.1.2"

# Use Redis adapter to run Action Cable in production
# gem "redis", ">= 4.0.1"

# Use Kredis to get higher-level data types in Redis. See: https://github.com/rails/kredis
# gem "kredis"

# Use Active Model has_secure_password. See: https://guides.rubyonrails.org/active_model_basics.html#securepassword
# gem "bcrypt", "~> 3.1.7"

# Windows does not include zoneinfo files, so bundle the tzinfo-data gem
gem "tzinfo-data", platforms: %i[windows jruby]

# Reduces boot times through caching; required in config/boot.rb
gem "bootsnap", require: false

# Use Active Storage variants. See: https://guides.rubyonrails.org/active_storage_overview.html#transforming-images
# gem "image_processing", "~> 1.2"

group :development, :test do
  # Debugging tools. See: https://guides.rubyonrails.org/debugging_rails_applications.html#debugging-with-the-debug-gem
  gem "debug", platforms: %i[mri windows]
  # Audits gems for known security defects (use config/bundler-audit.yml to ignore issues)
  gem "bundler-audit", require: false

  # Static analysis for security vulnerabilities [https://brakemanscanner.org/]
  gem "brakeman", require: false

  # Omakase Ruby styling [https://github.com/rails/rubocop-rails-omakase/]
  gem "rubocop-rails-omakase", require: false

end

group :development do
  # Use console on exception pages. See: https://github.com/rails/web-console
  gem "web-console"

  # Add speed badges. See: https://github.com/MiniProfiler/rack-mini-profiler
  # gem "rack-mini-profiler"

  # Speed up commands on slow machines / big apps. See: https://github.com/rails/spring
  # gem "spring"
end

group :test do
  # Use system testing. See: https://guides.rubyonrails.org/testing.html#system-testing
  gem "capybara"
  gem "selenium-webdriver"
end

# Authentication solution for Rails. See: https://github.com/heartcombo/devise
gem "devise", "~> 5.0"

# Simple calendar for Rails apps. See: https://github.com/excid3/simple_calendar
gem "simple_calendar", "~> 3.1"
