class Rental < ApplicationRecord
  def emoji
    icons = defined?(DUMPSTER_ICONS) ? DUMPSTER_ICONS : {}
    key =
      if respond_to?(:emoji_key) && emoji_key.present?
        emoji_key
      else
        title.to_s.strip[0]&.upcase
      end
    icons[key] || icons["default"] || "🗑️"
  end
end
