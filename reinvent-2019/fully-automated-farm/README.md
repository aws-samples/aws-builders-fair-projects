# Fully Automated Farm

## Overview
An important point in agriculture is to grow delicious crops efficiently at low cost.
In order to grow delicious crops, it is necessary to provide an optimal cultivation environment, and to provide appropriate amounts of water and nutrients at appropriate times.
Also, in order to carry out these tasks at low cost, a system for monitoring and automation is required.
In this demo, we propose a monitoring and automation solution using AWS IoT to provide an optimal cultivation environment.
By automated watering, we reduce and optimize the work load that occurs irregularly.
Furthermore, we propose a monitoring and automated system so that they can be dosed at best timing.

This demo shows fully automated watering to the fields by IoT.
Each field have several moisture sensors that constantly monitor the moisture in the soil at each location.
Therefore, if dry is observed on all the sensors of the field, the field is determined to be dry and watering is started automatically.
And watering is stopped automatically when the entire field is moisturized.
The sales-point is there is no code and database on the cloud side.
AWS IoT Events is used to control and manage devices and its state in this demo.


## Actual demo stand
![](./images/demo1.jpeg)

![](./images/demo2.jpeg)

![](./images/demo3.jpeg)


## Architecture Diagram
![Architecture Diagram](./images/Architecture.png)


## Models of AWS IoT Events
![Models of AWS IoT Events](./images/IoTEvents_models.png)


## BOM Software
1. Raspbian OS which can be installed [AWS IoT Greengrass](https://docs.aws.amazon.com/greengrass/latest/developerguide/what-is-gg.html#gg-platforms)
1. Python
1. [AWS IoT Greengrass](https://docs.aws.amazon.com/greengrass/latest/developerguide)
1. AWS Device SDK for Python


## BOM Hardware
|  No.  | Item image | Item name |       | Link |
| :---: | :--------: | :-------: | :---: | :---: |
|   1   | <img src="https://images-na.ssl-images-amazon.com/images/I/41NwqXwhxBL._AC_.jpg" width="200"> | Raspberry Pi 3 or 4 | 5 | |
|   2   | <img src="" width="200"> | LEGO Blocks | A Lot | |
|   3   | <img src="https://d2air1d4eqhwg2.cloudfront.net/images/814/500x500/85224b68-dd8f-4a37-a263-e7aad49af73b.jpg" width="200"> |　Grove Moisture sensor | 9 | [Link](https://www.switch-science.com/catalog/814/) |
|   4   | <img src="" width="200"> |　Clear case | 3 |  |
|   5   | <img src="https://d2air1d4eqhwg2.cloudfront.net/images/1629/500x500/906d6a8a-1c30-4c74-8ee3-87d853b5f1e7.jpg" width="200"> |　Grove LCD | 1 | [Link](https://www.switch-science.com/catalog/1629/) |
|   6   | <img src="https://images-na.ssl-images-amazon.com/images/I/6142jQq7R0L._AC_SL1005_.jpg" width="200"> |　Pump | 6 | [Link](https://www.amazon.co.jp/gp/product/B07D29YT2C/ref=ppx_yo_dt_b_asin_title_o01_s01?ie=UTF8&psc=1) |
|   7   | <img src="https://images-na.ssl-images-amazon.com/images/I/514zXX0Do-L._AC_SL1024_.jpg" width="200"> |　Water tank | 1 | [Link](https://www.amazon.co.jp/gp/product/B07VXKD77W/ref=ppx_yo_dt_b_asin_title_o01_s01?ie=UTF8&psc=1) |
|   8   | <img src="https://images-na.ssl-images-amazon.com/images/I/61NzWZXiXKL._AC_SL1001_.jpg" width="200"> |　DC Power | 1 | [Link](https://www.amazon.co.jp/gp/product/B0798JTWTD/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1) |
|   9   | <img src="https://images-na.ssl-images-amazon.com/images/I/718KB7M%2BmpL._AC_SL1200_.jpg" width="200"> |　Mechanical relay | 3 channels + | [Link](https://www.amazon.co.jp/dp/B07CKTJ8RF/ref=cm_sw_em_r_mt_dp_U_XIpVEb77MM227) |
|  10   | <img src="https://images-na.ssl-images-amazon.com/images/I/61ZepqPg-0L._AC_SL1100_.jpg" width="200"> |　Hose | 2 | [Link](https://www.amazon.co.jp/gp/product/B01D9SXY7K/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1) |
|  11   | <img src="" width="200"> |　LAN Cable | 10+ | [Link]() |
|  12   | <img src="https://images-na.ssl-images-amazon.com/images/I/61Rj1Nup7WL._SL1192_.jpg" width="200"> |　Cable | 1+ | [Link](https://www.amazon.co.jp/gp/product/B010SBSX4K/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1) |
|  13   | <img src="https://images-na.ssl-images-amazon.com/images/I/61hCN6aAF2L._AC_SL1001_.jpg" width="200"> |　PoE splitter | 10+ | [Link](https://www.amazon.co.jp/gp/product/B07MZC8RSH/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1) |
|  14   | <img src="https://images-na.ssl-images-amazon.com/images/I/71I5gqhhCmL._AC_SL1200_.jpg" width="200"> |　PoE Switching Hub | 1 | [Link](https://www.amazon.co.jp/gp/product/B07VMM39L7/ref=ppx_yo_dt_b_asin_title_o03_s01?ie=UTF8&psc=1) |
|  15   | <img src="https://images-na.ssl-images-amazon.com/images/I/71Z8NLw2I9L._SL1500_.jpg" width="200"> |　T Joint for Hose | 5+ | [Link](https://www.amazon.co.jp/gp/product/B01LYHWV3F/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1) |
|  16   | <img src="https://images-na.ssl-images-amazon.com/images/I/41Q%2B5LzCjNL._AC_.jpg" width="200"> |　Light Sensor | 1 | [Link](https://www.amazon.co.jp/gp/product/B00CHHVPNA/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1) |
|  17   | <img src="" width="200"> |　SD card for Raspberry Pi | Same as Raspberry Pi | [Link]() |
|  18   | <img src="https://images-na.ssl-images-amazon.com/images/I/61kSF3xWmtL._SL1000_.jpg" width="200"> |　Elbow for Hose | 6+ | [Link](https://www.amazon.co.jp/gp/product/B01LWV8PVB/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1) |
|  19   | <img src="https://images-na.ssl-images-amazon.com/images/I/61FJ4XUJZDL._AC_SL1000_.jpg" width="200"> |　Grove Pi | 3+ | [Link](https://www.amazon.co.jp/gp/product/B07H9NJQY2/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&psc=1) |


## Authors
- Shota Iizuka: [iizus@amazon.co.jp](iizus@amazon.co.jp)
- Satoshi Watanabe: [watsatos@amazon.co.jp](watsatos@amazon.co.jp)
- Tatsuhiro Iida: [tatsiida@amazon.co.jp](tatsiida@amazon.co.jp)


# License
This library is licensed under the Apache 2.0 License.
