# [Odoo](https://www.odoo.com "Odoo's Homepage") Custom Module

This module is for testing/sample only!

## Installation procedure

##### 1. Clone the module to your custom addons directory using _Git_
```
cd odoo/custom_addons
```
```
sudo git clone https://github.com/kmcalda/custom_module.git
```
##### 2. Restart odoo service
```
sudo service odoo-server restart
```

##### 3. Go to your odoo webpage then make sure that the _developer mode_ is activated under _Settings>General Settings_

##### 4. Update apps list by going to Apps menu then click _Update Apps List_

##### 5. Look for the module named _"Custom Module"_ then install

## Grabbing updates

##### 1. Make sure you are inside the module directory
```
cd /odoo/custom_addons/custom_module
```
##### 2. Use the command git pull to fetch and merge
```
git pull
```
##### 3. Same with the _Installation procedure_, start from _2 to 4_
##### 4. Look for the module name then _update_

## Task list
- [x] ***Contacts***: Add Region field in Fed. States
- [x] ***Contacts***: Add Region field in contact form
- [x] ***Contacts***: Move Internal Reference(Renamed to Reference) to place beside Region field before the Country field
- [x] ***Contacts***: Change Tax ID name to TIN
- [x] ***Contacts***: TIN and Reference are now unique
- [x] ***Contacts***: Mandatory field (Street,Street2,City,State,Zip,Region,Reference,TIN)
- [x] ***Sales***: Unit Price in Orders form is now uneditable
- [x] ***Inventory***: Mandatory field (Source Document in Transfer form)
- [x] ***Inventory***: Internal Reference in Products form is now unique
- [x] ***Invoicing***: Notebook tag is hidden if not a Billing Administrator
- [ ] ***Inventory***: Detailed Operation must include field to enter expiry date
- [ ] ***Inventory***: Detailed Operation in Transfer Receipt should autoget Item for assigning lot number
- [x] ***Contacts***: 12-digit TIN on Contacts (no special character or hypen)
- [x] ***Contacts***: Region should not be editable 
- [ ] ***Inventory***: Lot number in detailed operations should be mandatory
- [ ] ***Inventory***: Customize receiving to allow input of expiry date (best before date field)
