'''

Para usar a API crie  a variavel de ambiente com a chave de acesso a API


   $> export DO_ACCESS_TKN='TOKEN_LETTER_SOUP_HERE'

'''

import digitalocean
import os


class Droplets(object):

    def __init__(self, token=None):
        # params takes precedence over enviroment vars

        if not token:
            self.token = os.getenv('DO_ACCESS_TKN')
        else:
            self.token = token

    def get_droplets(self):

        manager = digitalocean.Manager(token=self.token)
        drops = None
        try:
            drops = manager.get_all_droplets()
        except digitalocean.DataReadError:
            pass

        return drops

    def show_droplets(self):
        ds = self.get_droplets()
        for d in ds:
            print(f'action_ids: {d.action_ids}')
            print(f'backup_ids: {d.backup_ids}')
            print(f'backups: {d.backups}')
            print(f'created_at: {d.created_at}')
            print(f'disk: {d.disk}')
            print(f'end_point: {d.end_point}')
            print(f'features: {d.features}')
            print(f'id: {d.id}')
            print(f'image: {d.image}')
            print(f'ip_address: {d.ip_address}')
            print(f'ip_v6_address: {d.ip_v6_address}')
            print(f'ipv6: {d.ipv6}')
            print(f'kernel: {d.kernel}')
            print(f'locked: {d.locked}')
            print(f'memory: {d.memory}')
            print(f'monitoring: {d.monitoring}')
            print(f'name: {d.name}')
            print(f'networks: {d.networks}')
            print(f'next_backup_window: {d.next_backup_window}')
            print(f'private_ip_address: {d.private_ip_address}')
            print(f'private_networking: {d.private_networking}')
            print(f'private_networking: {d.private_networking}')
            print(f'region: {d.region}')
            print(f'size: {d.size}')
            print(f'size_slug: {d.size_slug}')
            print(f'snapshot_ids: {d.snapshot_ids}')
            print(f'ssh_keys: {d.ssh_keys}')
            print(f'status: {d.status}')
            print(f'tags: {d.tags}')
            print(f'token: {d.token}')
            print(f'user_data: {d.user_data}')
            print(f'vcpus: {d.vcpus}')
            print(f'volume_ids: {d.volume_ids}')
            print(f'volumes: {d.volumes}')
            print(f'--------------------------------')

# # DropLet Attributs
# action_ids
# backup_ids
# backups
# created_at
# disk
# end_point
# features
# id
# image
# ip_address
# ip_v6_address
# ipv6
# kernel
# locked
# memory
# monitoring
# name
# networks
# next_backup_window
# private_ip_address
# private_networking
# private_networking
# region
# size
# size_slug
# snapshot_ids
# ssh_keys
# status
# tags
# token
# user_data
# vcpus
# volume_ids
# volumes

# # droplet functions
# change_kernel()
# create()
# create_multiple()
# destroy()
# disable_backups()
# enable_backups()
# enable_ipv6()
# enable_private_networking()
# get_action()
# get_actions()
# get_data()
# get_events()
# get_kernel_available()
# get_object()
# get_snapshots()
# get_timeout()
# load()
# power_cycle()
# power_off()
# power_on()
# reboot()
# rebuild()
# rename()
# reset_root_password()
# resize()
# restore()
# shutdown()
# take_snapshot()
# update_volumes_data()
#