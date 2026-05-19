function applyJob(companyId) {
    if(confirm('Are you sure you want to apply for this company?')) {
        fetch('/apply/' + companyId, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                alert(data.message);
                location.reload(); // Reload to update button states
            } else {
                alert('Failed: ' + data.message);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while applying.');
        });
    }
}

function updateStatus(applicationId, newStatus) {
    const formData = new FormData();
    formData.append('status', newStatus);

    fetch('/admin/applications/update/' + applicationId, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            // Update badge color visually
            const badge = document.getElementById('status-badge-' + applicationId);
            if (badge) {
                badge.textContent = newStatus;
                badge.className = 'badge';
                if(newStatus === 'Applied') badge.classList.add('bg-primary');
                else if(newStatus === 'Selected') badge.classList.add('bg-success');
                else if(newStatus === 'Rejected') badge.classList.add('bg-danger');
            }
            // Optional: show a small toast or message instead of alert
            console.log('Status updated successfully');
        } else {
            alert('Failed to update status: ' + data.message);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred while updating status.');
    });
}
