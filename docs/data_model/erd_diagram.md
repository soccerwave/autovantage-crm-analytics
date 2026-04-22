Table dim\_date {

&#x20; date\_key int \[pk]

&#x20; full\_date date

}



Table dim\_dealer {

&#x20; dealer\_id varchar \[pk]

&#x20; region varchar

&#x20; brand varchar

}



Table dim\_vehicle {

&#x20; vehicle\_id varchar \[pk]

&#x20; brand varchar

&#x20; model\_name varchar

}



Table dim\_contact {

&#x20; contact\_id varchar \[pk]

&#x20; full\_name varchar

}



Table dim\_campaign {

&#x20; campaign\_id varchar \[pk]

&#x20; campaign\_type varchar

}



Table dim\_account {

&#x20; account\_id varchar \[pk]

&#x20; account\_type varchar

&#x20; primary\_contact\_id varchar

}



Table fact\_leads {

&#x20; lead\_id varchar \[pk]

&#x20; created\_date\_key int

&#x20; dealer\_id varchar

&#x20; contact\_id varchar

&#x20; vehicle\_interest varchar

}



Table bridge\_lead\_campaign {

&#x20; lead\_id varchar

&#x20; campaign\_id varchar

}



Table fact\_opportunities {

&#x20; opportunity\_id varchar \[pk]

&#x20; lead\_id varchar

&#x20; account\_id varchar

&#x20; vehicle\_id varchar

&#x20; dealer\_id varchar

&#x20; close\_date\_key int

}



Table fact\_orders {

&#x20; order\_id varchar \[pk]

&#x20; opportunity\_id varchar

&#x20; order\_date\_key int

}



Table fact\_service\_cases {

&#x20; case\_id varchar \[pk]

&#x20; contact\_id varchar

&#x20; account\_id varchar

&#x20; vehicle\_id varchar

&#x20; dealer\_id varchar

&#x20; open\_date\_key int

}



Table fact\_customer\_feedback {

&#x20; feedback\_id varchar \[pk]

&#x20; case\_id varchar

&#x20; survey\_date\_key int

}



Ref: dim\_account.primary\_contact\_id > dim\_contact.contact\_id

Ref: fact\_leads.created\_date\_key > dim\_date.date\_key

Ref: fact\_leads.dealer\_id > dim\_dealer.dealer\_id

Ref: fact\_leads.contact\_id > dim\_contact.contact\_id

Ref: fact\_leads.vehicle\_interest > dim\_vehicle.vehicle\_id

Ref: bridge\_lead\_campaign.lead\_id > fact\_leads.lead\_id

Ref: bridge\_lead\_campaign.campaign\_id > dim\_campaign.campaign\_id

Ref: fact\_opportunities.lead\_id > fact\_leads.lead\_id

Ref: fact\_opportunities.account\_id > dim\_account.account\_id

Ref: fact\_opportunities.vehicle\_id > dim\_vehicle.vehicle\_id

Ref: fact\_opportunities.dealer\_id > dim\_dealer.dealer\_id

Ref: fact\_opportunities.close\_date\_key > dim\_date.date\_key

Ref: fact\_orders.opportunity\_id > fact\_opportunities.opportunity\_id

Ref: fact\_service\_cases.contact\_id > dim\_contact.contact\_id

Ref: fact\_service\_cases.account\_id > dim\_account.account\_id

Ref: fact\_service\_cases.vehicle\_id > dim\_vehicle.vehicle\_id

Ref: fact\_service\_cases.dealer\_id > dim\_dealer.dealer\_id

Ref: fact\_customer\_feedback.case\_id > fact\_service\_cases.case\_id

