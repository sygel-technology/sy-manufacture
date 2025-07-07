To use this module, you need to:

1. Create a Work Center:
    Go to Manufacturing > Configuration > Work Centers and create a new work center or edit an existing one.

2. Add Components:
    In the new Components tab of the work center form, add the required products and their fixed quantities.

3. Link the Work Center to a BoM Operation
    Go to Manufacturing > Products > Bills of Materials and edit the BoM of a product.
    In the Operations tab, add an operation and assign the desired work center.

4. Create a Manufacturing Order
    Go to Manufacturing > Operations > Manufacturing Orders and create a new MO for the product with the configured BoM.

5. Confirm the Manufacturing Order
    Upon confirmation, in the Components tab of the MO, the system will include:

    - The standard BoM components.
    - The additional components defined in the work center(s), with their exact configured quantities (not scaled by production quantity).
