async function editInterval(id, currentVal) {

    let newVal = prompt("Enter new interval (seconds):", currentVal);

    if (newVal === null || newVal.trim() === "") return;
    newVal = parseInt(newVal);
    if (isNaN(newVal) || newVal < 1) {
        alert("Please use valid time.");
        return;
    }

    try {
        const response = await fetch(`/update_interval/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ time_interval: newVal })
        });

        if (response.ok) {
            const row = document.getElementById(`row-${id}`);
            const cell = row.querySelector('.interval-value');
            cell.textContent = newVal;

            const btn = row.querySelector('.btn-change-interval');
            btn.setAttribute('onclick', `editInterval('${id}', '${newVal}')`); //update too so it has new value
        } else {
            alert("Error updating.");
        }
    } catch (error) {
        console.error('Error:', error);
        alert("Server error.");
    }
}