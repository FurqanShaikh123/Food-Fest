const API_BASE = "http://127.0.0.1:5000";

let orderItems = [];
let userName = "";
let paymentMethod = "Cash";

async function loadMenu() {
    const res = await fetch(`${API_BASE}/menu`);
    const menu = await res.json();
    const container = document.querySelector("#menu-items");
    container.innerHTML = "";
    menu.forEach(item => {
        const div = document.createElement("div");
        div.innerHTML = `
            <h3>${item.name}</h3>
            <p>${item.description}</p>
            <p>$${item.price}</p>
            <button onclick="addItem(${item.id}, '${item.name}', ${item.price})">Add to Order</button>
        `;
        container.appendChild(div);
    });
}

function addItem(id, name, price) {
    orderItems.push({ id, name, price });
    renderOrder();
}

function removeItem(index) {
    orderItems.splice(index, 1);
    renderOrder();
}

function renderOrder() {
    const container = document.querySelector("#order-summary");
    container.innerHTML = "";
    orderItems.forEach((item, index) => {
        const div = document.createElement("div");
        div.innerHTML = `${item.name} - $${item.price} <button onclick="removeItem(${index})">Remove</button>`;
        container.appendChild(div);
    });
}

function setPayment(method) {
    paymentMethod = method;
}

async function placeOrder() {
    userName = document.querySelector("#user-name").value.trim();
    if (!userName) return alert("Please enter your name");
    if (orderItems.length === 0) return alert("Please add items to order");

    const res = await fetch(`${API_BASE}/order`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: userName, items: orderItems, payment_method: paymentMethod })
    });
    const data = await res.json();
    alert(data.message);
    orderItems = [];
    renderOrder();
    document.querySelector("#user-name").value = "";
}
