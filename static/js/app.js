
// D3Khan Blog - minimal JS
// Form validation enhancements
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.form-input, .form-textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.closest('.form-field').style.borderColor = '#1a73e8';
        });
        input.addEventListener('blur', () => {
            input.closest('.form-field').style.borderColor = '#dadce0';
        });
    });
});
