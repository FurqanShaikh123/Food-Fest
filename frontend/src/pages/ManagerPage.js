const API_BASE = "http://127.0.0.1:5000";

async function loadOrders() {
    const res = await fetch(`${API_BASE}/orders`);
    const orders = await res.json();
    const container = document.querySelector("#orders-container");
    container.innerHTML = "";
    orders.forEach(o => {
        const div = document.createElement("div");
        div.innerHTML = `
            <h4>Order #${o.id} - ${o.username}</h4>
            <p>Items: ${o.items.map(i => i.name).join(", ")}</p>
            <p>Status: ${o.status}</p>
            <button onclick="updateStatus(${o.id}, 'Preparing')">Preparing</button>
            <button onclick="updateStatus(${o.id}, 'Ready')">Ready</button>
        `;
        container.appendChild(div);
    });
}

async function updateStatus(id, status) {
    const res = await fetch(`${API_BASE}/orders/${id}/status`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status })
    });
    const data = await res.json();
    alert(data.message);
    loadOrders();
}
