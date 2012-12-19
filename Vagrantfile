# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32"
  config.vm.network :hostonly, "11.22.33.44"
  config.vm.customize ["modifyvm", :id, "--name", "FreedomFoneVM"]
end
