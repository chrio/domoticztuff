#!/bin/bash
curl 'http://192.168.1.10/YamahaRemoteControl/ctrl' --data-binary '<YAMAHA_AV cmd="PUT"><Main_Zone><Power_Control><Power>Suspend</Power></Power_Control></Main_Zone></YAMAHA_AV>'