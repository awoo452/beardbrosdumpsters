class AddEmojiKeyToRentals < ActiveRecord::Migration[7.1]
  def change
    add_column :rentals, :emoji_key, :string
  end
end
