// function validation(values) {
//     let error = {};
    
//     // name validation
//     if (values.username === "") {
//         error.username = "Name can't be empty";
//     } else {
//         error.username = "";
//     }
    
    
//     // password validation
//     if (values.password === "") {
//         error.password = "Password can't be empty";
//     } else if (values.password.length < 8) {
//         error.password = "Password must be at least 8 characters";
//     } else {
//         error.password = "";
//     }
    
//     return error;
// }

// export default validation;

function validation(values) {
    let errors = {};
  
    // Username validation
    if (!values.username || values.username.trim() === "") {
      errors.username = "Username can't be empty";
    } else {
      errors.username = "";
    }
  
    // Password validation
    if (!values.password || values.password.trim() === "") {
      errors.password = "Password can't be empty";
    } else if (values.password.length < 8) {
      errors.password = "Password must be at least 8 characters";
    } else {
      errors.password = "";
    }
  
    return errors;
  }
  
  export default validation;