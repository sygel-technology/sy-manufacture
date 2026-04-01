To use this module, you need to:

1. Go to Manufacturing / Operations / Manufacturing Orders
2. Create a MRP Order or open one in "Confirmed" in state
3. Click on the "Start" button
4. You will see the "Return to Confirmed" button. Click on it, the MRP Order will return to the confirmed status.

NOTE: Actually, not all MRP Orders that have the 'in progress' state can directly go back to the 'confirmed' status. For example, MRP Orders with produced quantities, or those with Work Orders that are finished or in progress. This is because the state field is computed, and these specific cases force the state to remain "in progress".
