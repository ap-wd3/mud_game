function validation(values) {
    let error = {};
    const email_pattern = /\S+@\S+\.\S+/;
    
    // name validation
    if (values.username === "") {
        error.username = "Name can't be empty";
    } else {
        error.username = "";
    }
    
    // email validation
    if (values.email === "") {
        error.email = "Email can't be empty";
    } else if (!email_pattern.test(values.email)) {
        error.email = "Please use a valid email address";
    } else {
        error.email = "";
    }
    
    // password validation
    if (values.password === "") {
        error.password = "Password can't be empty";
    } else if (values.password.length < 8) {
        error.password = "Password must be at least 8 characters";
    } else {
        error.password = "";
    }
    
    // password confirmation validation
    if (values.password_confirmation === "") {
        error.password_confirmation = "Please confirm password";
    } else if (values.password_confirmation !== values.password) {
        error.password_confirmation = "Password does not match";
    } else {
        error.password_confirmation = "";
    }
    
    return error;
}

export default validation;