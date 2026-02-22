namespace :db do
  desc "Reset PostgreSQL sequences to max(id) for all tables"
  task reset_sequences: :environment do
    connection = ActiveRecord::Base.connection

    connection.tables.each do |table|
      next if %w[schema_migrations ar_internal_metadata].include?(table)

      pk = connection.primary_key(table)
      next if pk.nil?

      sequence = connection.default_sequence_name(table, pk)
      next if sequence.nil?

      max_id = connection.select_value("SELECT MAX(#{pk}) FROM #{table}")
      next if max_id.nil?

      connection.execute(
        "SELECT setval('#{sequence}', #{max_id}, true)"
      )
    end
  end
end
