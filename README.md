# dynamic_context_plus

## Summary
An extension for oobabooga's [Text Generation WebUI](https://github.com/oobabooga/text-generation-webui) which gives conversations more context.

It's based on the excellent [dynamic_context](https://github.com/elPatrixF/dynamic_context) extension by elPatrixF.

### Usage option 1
Set the "auto_append" in config to "true" and it will automatically inject a dynamic sentence into the context.

Just modify **settings.yaml** with the config `dynamic_context_plus-auto_append: true`.

You won't have to add anything to the character files if you use this option.

### Usage option 2
Add any of the following template strings to your character file and they will be replaced.
- {{location}} with the given location
- {{temperature}} with the selected temperature
- {{weather}} with the selected weather
- {{time}} with the current time
- {{time_of_day}} with "morning", "afternoon", "evening" or "night"
- {{date}} with the current data
- {{season}} with the "spring", "summer", "autumn" or "winter" (based on wester hemisphere)
- {{weekday}} with the day of the week

### Additional notes
It can also append the current time or date as extra information at the end of the prompt.
