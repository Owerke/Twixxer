"use strict";

function validate_email(email) {
    let re = new RegExp("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$");
    // If the email is a match, return true.
    if (re.test(email.toLowerCase())) {
        return true;
    }
    return false;
}

function validate_by_regex(text, regexStr) {
    let regex = new RegExp(regexStr);
    if (regex.test(text)) {
        return true;
    }
    return false;
}

function validate_text_length(text, minLength, maxLength) {
    if (text.length < minLength || text.length > maxLength) {
        return false;
    }
    return true;
}

function validate_integer_range(number, minValue, maxValue) {
    if (number < minValue || number > maxValue) {
        return false;
    }
    return true;
}

// ##############################
function validate(callback) {
    const form = event.target
    console.log(form)
    const validate_error_color = "rgba(240, 130, 240, 0.2)"
    get_all_elements("[data-validate]", form).forEach(function (element) {
        element.classList.remove("validate_error")
        element.style.backgroundColor = "white"
    })
    let text = ""
    get_all_elements("[data-validate]", form).forEach(function (element) {
        switch (element.getAttribute("data-validate")) {
            case "str":
                // Validate string length
                let minLength = parseInt(element.getAttribute("data-min"));
                let maxLength = parseInt(element.getAttribute("data-max"));
                text = element.value;
                if (!validate_text_length(text, minLength, maxLength)) {
                    element.classList.add("validate_error");
                    element.style.backgroundColor = validate_error_color;
                }
                break;
            case "int":
                // Validate if integer is between values
                let minValue = parseInt(element.getAttribute("data-min"));
                let maxValue = parseInt(element.getAttribute("data-max"));
                let number = parseInt(element.value);
                // If it's not a number, or it's out of range, we return error
                if (isNaN(number) || validate_integer_range(number, minValue, maxValue)) {
                    element.classList.add("validate_error");
                    element.style.backgroundColor = validate_error_color;
                }
                break;
            case "email":
                // Validate if string is email
                let email = element.value.toLowerCase();
                if (!validate_email(email)) {
                    element.classList.add("validate_error");
                    element.style.backgroundColor = validate_error_color;
                }
                break;
            case "re":
                // Validate if string matches regex
                let regexStr = element.getAttribute("data-re")
                text = element.value
                if (!validate_by_regex(text, regexStr)) {
                    element.classList.add("validate_error")
                    element.style.backgroundColor = validate_error_color
                }
                break;
            case "match":
                // FIXME: WTF
                // name = element.getAttribute("data-match-name").queryselector(form).value
                if (element.value != get_one_element(`[name='${element.getAttribute("data-match-name")}']`, form).value) {
                    element.classList.add("validate_error")
                    element.style.backgroundColor = validate_error_color
                }
                break;
        }
    })
    if (!get_one_element(".validate_error88", form)) { callback(); return }
    // _one(".validate_error", form).focus()
}

// ##############################
function clear_validate_error() {
    // event.target.classList.remove("validate_error")
    // event.target.value = ""
}
