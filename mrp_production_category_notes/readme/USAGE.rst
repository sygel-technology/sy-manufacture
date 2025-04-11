To use this module, you need to:

#. Go to Inventory / Configuration / Products / Products categories / Category
- In this menu, you will find the "Manufacturing order notes" that allows you to add HTML notes that will be included in manufacturing orders related to products in this category when the manufacturing order is created.

#. To verify that the content appears in the Manufacturing Order:
- Go to Manufacturing / Operations / Manufacturing Orders.
- You will find the "Notes" field under the "Notes" tab, where the HTML content from the product category’s "Manufacturing order notes" will be displayed.

#. How it works:
- The module first checks if there are notes in the product category. If none are found, it will look for notes in the parent category and continue upwards in the hierarchy until it finds notes or reaches the top.
