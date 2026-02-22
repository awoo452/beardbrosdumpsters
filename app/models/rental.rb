class Rental < ApplicationRecord
  def emoji
    icons = defined?(DUMPSTER_ICONS) ? DUMPSTER_ICONS : {}
    key = title.to_s.strip[0]&.upcase
    icons[key] || icons["default"] || "🗑️"
  end
end
