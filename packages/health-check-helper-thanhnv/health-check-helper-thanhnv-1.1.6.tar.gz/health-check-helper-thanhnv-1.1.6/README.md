# Help Tool


## Before Run

* Creat file input as check_port_list.txt : [example](check_port_list.txt)
  * Format each line : {host},{ports}
    * {host}: host name or ip ex:  10.1.30.41
    * {ports}: could be
      * a list port seperated by space (" ") ex : 82 83 
      * or a range({start_number}-{end_number}) ex : 100-200
    * example :
      * 10.1.44.16,8020
      * 10.1.44.16,8020 585 3452
      * 10.1.44.16,8000-8500

**check_port_list.txt** file example
    
```text
10.1.30.41,88
10.1.44.16,8020 585
10.1.30.41,50000-56000
```
        
## Run

>help_tool check_ports -i check_port_list.txt -o check_port_result.json -n 100

## After Run

File result in [check_socket_result.json](_check_port_result.json)

```json
{
    "open": {
        "10.1.30.41": [
            "88",
            "8050",
            "8080-8081"
 
        ],
        "10.1.44.16": [
            "8020"
        ],
        "10.1.44.17": [
            "8020"
        ]
    },
    "close": {
        "10.1.30.41": [
            "50001-51999",
            "52001-56000"
        ]
    }
}
```
Note:
 - key "open" contain host and ports have already opened
 - key "close" contain host and ports have still closed 
    

