# Como crear un portal cautivo #

Pasos:
  1. cambiar configuracion interface
  1. arrancar hostapd -d /etc/hostapd/hostapd.conf
  1. Arrarcar  bash redirect\_trafic.sh
  1. arrancar:  dnsmasq -dq

## Configuraciones ##
nuevas interfaces:
```

allow-hotplug wlan0

iface wlan0 inet static

address 192.168.42.1
netmask 255.255.255.0
gateway 19.168.1.1

```

/etc/hostapd/hostapd.conf
```

interface=wlan0
#driver=nl80211
#driver=rtl871xdrv
ssid=My_AP
hw_mode=g
channel=6
auth_algs=1
wmm_enabled=0
```

/etc/dnsmasq.conf
```


interface=wlan0
#driver=nl80211
#driver=rtl871xdrv
ssid=My_AP
hw_mode=g
channel=6
auth_algs=1
wmm_enabled=0

```

redirect\_trafic.sh
```

sudo iptables -t mangle -N internet
sudo iptables -t mangle -A PREROUTING -p tcp -i wlan0 --dport 443 -j internet
sudo iptables -t mangle -A PREROUTING -p tcp -i wlan0 --dport 80 -j internet
sudo iptables -t mangle -A internet -j MARK --set-mark 99
sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp -m mark --mark 99 --dport 80 -j DNAT --to-destination 192.168.42.1

```