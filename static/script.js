document.addEventListener('DOMContentLoaded', () => {
    const API_URL = 'http://localhost:5000';
    const productList = document.getElementById('productList');
    const addProductForm = document.getElementById('addProductForm');

    // --- Fetch and display all products ---
    const fetchProducts = async () => {
        try {
            const response = await fetch(`${API_URL}/products`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const products = await response.json();

            // Clear the list before rendering
            productList.innerHTML = '';

            if (products && products.length > 0) {
                products.forEach(product => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <div class="product-info">
                            <span>${product.name}</span>
                            <span class="price">$${product.price.toFixed(2)}</span>
                        </div>
                        <div class="product-actions">
                            <button class="edit-btn" data-id="${product.id}" data-name="${product.name}" data-price="${product.price}">Edit</button>
                            <button class="delete-btn" data-id="${product.id}">Delete</button>
                        </div>
                    `;
                    productList.appendChild(li);
                });
            } else {
                productList.innerHTML = '<li>No products found.</li>';
            }
        } catch (error) {
            console.error("Failed to fetch products:", error);
            productList.innerHTML = '<li>Error loading products.</li>';
        }
    };

    // --- Handle adding a new product ---
    addProductForm.addEventListener('submit', async (event) => {
        event.preventDefault(); 

        // --- MODIFICATION START ---
        const submitButton = addProductForm.querySelector('button');
        const originalButtonText = submitButton.textContent;
        // --- MODIFICATION END ---
        
        const name = document.getElementById('name').value;
        const price = parseFloat(document.getElementById('price').value);

        if (!name || isNaN(price)) {
            alert('Please enter valid product name and price.');
            return;
        }

        // --- MODIFICATION START ---
        submitButton.disabled = true;
        submitButton.textContent = 'Adding...';
        // --- MODIFICATION END ---

        try {
            const response = await fetch(`${API_URL}/products`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, price }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            addProductForm.reset();
            await fetchProducts();

        } catch (error) {
            console.error("Failed to add product:", error);
            alert('Failed to add product.');
        } finally {
            // --- MODIFICATION START ---
            // This block always runs, ensuring the button is restored.
            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
            // --- MODIFICATION END ---
        }
    });

    // Consolidated event listener for both Edit and Delete actions
    productList.addEventListener('click', async (event) => {
        const target = event.target;
        
        // --- Handle Edit Product ---
        if (target.classList.contains('edit-btn')) {
            const originalButtonText = target.textContent;
            const productId = target.dataset.id;
            const currentName = target.dataset.name;
            const currentPrice = target.dataset.price;

            const newName = prompt("Enter the new product name:", currentName);
            const newPriceStr = prompt("Enter the new price:", currentPrice);

            if (newName === null || newPriceStr === null) {
                return; // User cancelled
            }

            const newPrice = parseFloat(newPriceStr);

            if (!newName.trim() || isNaN(newPrice)) {
                alert('Invalid name or price. Please try again.');
                return;
            }
            
            // --- MODIFICATION START ---
            target.disabled = true;
            target.textContent = 'Editing...';
            // --- MODIFICATION END ---

            try {
                const response = await fetch(`${API_URL}/products/${productId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name: newName, price: newPrice }),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                await fetchProducts(); 
            } catch (error) {
                console.error("Failed to update product:", error);
                alert('Failed to update product.');
            } finally {
                // --- MODIFICATION START ---
                target.disabled = false;
                target.textContent = originalButtonText; // Restores to "Edit"
                // --- MODIFICATION END ---
            }
        }

        // --- Handle Delete Product ---
        if (target.classList.contains('delete-btn')) {
            const originalButtonText = target.textContent;
            const productId = target.dataset.id;

            if (!confirm('Are you sure you want to delete this product?')) {
                return;
            }
            
            // --- MODIFICATION START ---
            target.disabled = true;
            target.textContent = 'Deleting...';
            // --- MODIFICATION END ---

            try {
                const response = await fetch(`${API_URL}/products/${productId}`, {
                    method: 'DELETE',
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                await fetchProducts(); 
            } catch (error) {
                console.error("Failed to delete product:", error);
                alert('Failed to delete product.');
            } finally {
                // --- MODIFICATION START ---
                // This is a safety measure. If deletion fails, the button is restored.
                // If it succeeds, the element is removed anyway.
                target.disabled = false;
                target.textContent = originalButtonText; // Restores to "Delete"
                // --- MODIFICATION END ---
            }
        }
    });

    // Initial fetch of products when the page loads
    fetchProducts();
});