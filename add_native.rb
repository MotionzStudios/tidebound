require 'xcodeproj'
proj = Xcodeproj::Project.open('ios/App/App.xcodeproj')
target = proj.targets.find { |t| t.name == 'App' }
group = proj.main_group['App'] || proj.main_group.new_group('App', 'App')
synced = target.respond_to?(:file_system_synchronized_groups) && !(target.file_system_synchronized_groups || []).empty?
puts "synchronized groups: #{synced}"
unless synced
  %w[GameCenterPlugin.swift MyViewController.swift].each do |f|
    ref = group.new_file(f)
    target.source_build_phase.add_file_reference(ref)
  end
end
group.new_file('App.entitlements') unless synced
target.build_configurations.each { |c| c.build_settings['CODE_SIGN_ENTITLEMENTS'] = 'App/App.entitlements' }
proj.save
puts "native files added"
