function validation(values) {
    let error = {};
    const email_pattern = /\S+@\S+\.\S+/;
    
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
    } else {
        error.password = "";
    }
    
    return error;
}

export default validation;