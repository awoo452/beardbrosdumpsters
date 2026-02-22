class Rental < ApplicationRecord
  def emoji
    icons = defined?(DUMPSTER_ICONS) ? DUMPSTER_ICONS : {}
    key = respond_to?(:emoji_key) ? emoji_key : nil
    icons[key] || icons["default"] || "🗑️"
  end
end
