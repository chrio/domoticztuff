-- Morgonkaffe script
-- Starta bryggaren vid en viss tidpunkt om dummydevicen 'Morgonkaffe' är på

time = os.date("*t")
commandArray = {}

-- När ska Kaffebryggaren startas ifall Morgonkaffe är påslagen?
HH=6
MM=10

if devicechanged ~= nil then
    -- Morgonkaffe DEVICE event

    if (time.hour >= 20) or (time.hour <= 4) then
        -- Om klockan är mellan 20:00 och 04:59
        if devicechanged['Kaffebryggaren'] == "On" then
            -- och kaffebryggaren slogs på
            
            if (otherdevices['Morgonkaffe'] == "Off") then
                commandArray['Morgonkaffe'] = "On"  -- slå på dummy devicen
                commandArray['Kaffebryggaren'] = "Off" -- av med bryggaren igen
                commandArray['SendNotification']='Sådär#Då är morgonkaffet laddat och klart'
                
            elseif (otherdevices['Morgonkaffe'] == "On") then
                commandArray['Morgonkaffe'] = "Off"  -- av med dummy devicen
                commandArray['SendNotification']='Okej#morgonkaffet är avstängt'
            end
        end
    end
else
    -- Morgonkaffe TIME event
    if (time.hour == HH) and (time.min == MM) and (otherdevices['Morgonkaffe'] == "On") then
        commandArray['Morgonkaffe'] = "Off" -- av med dummy devicen
        commandArray['Kaffebryggaren'] = "On FOR 20" -- bryggaren på i 20 minuter
        commandArray['SendNotification']='Godmorgon#Kaffet är snart klart'
    end

end

return commandArray
