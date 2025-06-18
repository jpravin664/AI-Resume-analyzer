document.addEventListener('DOMContentLoaded', function() {
    const resumeForm = document.getElementById('resumeForm');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = document.getElementById('btnText');
    const loadingSpinner = document.getElementById('loadingSpinner');
    
    if (resumeForm) {
        resumeForm.addEventListener('submit', function() {
            // Show loading state
            btnText.textContent = 'Analyzing...';
            loadingSpinner.classList.remove('d-none');
            analyzeBtn.disabled = true;
            
            // Form will submit naturally
        });
    }
    
    // File input validation
    const resumeInput = document.getElementById('resume');
    if (resumeInput) {
        resumeInput.addEventListener('change', function() {
            validateFileInput(this);
        });
    }
    
    function validateFileInput(input) {
        const allowedExtensions = ['pdf', 'docx', 'doc', 'txt'];
        const maxSizeInMB = 16;
        const maxSizeInBytes = maxSizeInMB * 1024 * 1024;
        
        if (input.files && input.files[0]) {
            const file = input.files[0];
            const fileExtension = file.name.split('.').pop().toLowerCase();
            
            // Check file type
            if (!allowedExtensions.includes(fileExtension)) {
                alert(`Invalid file type. Please upload a ${allowedExtensions.join(', ')} file.`);
                input.value = '';
                return false;
            }
            
            // Check file size
            if (file.size > maxSizeInBytes) {
                alert(`File size exceeds ${maxSizeInMB}MB limit. Please upload a smaller file.`);
                input.value = '';
                return false;
            }
            
            return true;
        }
        
        return false;
    }
});