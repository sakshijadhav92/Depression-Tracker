console.log("js loaded");

function signup_validation(){
    flag=true;
    message="";

    let password=document.getElementById("pa").value;
    let rpassword=document.getElementById("rpa").value;
    let email=document.getElementById("eml").value;
    let aadhar=document.getElementById("a").value;
    let fname=document.getElementById("fn").value;
    let lname=document.getElementById("ln").value;
    let contact=document.getElementById("c").value;
    let address=document.getElementById("txt").value;
    let gender=document.getElementsByName("gender");

    let count=0;
    for( let i=0;i<gender.length;i++){
        if(gender[i].checked){
            count++;
        }
    }
    if(count==0){
        flag=false;
        message+="No gender is selected\n";
    }

    let onlyalphabets=/^[A-Za-z]+$/
    let onlynumbers=/^[0-9]+$/

    if(password!=rpassword){
        flag=false;
        message+="Password and retyped password doesnot match\n"
    }
    if(contact.length!=10){
        flag=false;
        message+="Invalid contact\n"
    }
    if(aadhar.length!=12){
        flag=false;
        message+="Invalid aahar number\n"
    }
    if(!onlyalphabets.test(fname) || !onlyalphabets.test(lname)){
        flag=false;
        message+="name cannot contain numbers \n"
    }
    if(!onlynumbers.test(contact)){
        flag=false;
        message+="Contact field should only be having numeric values \n"
    }
    if(!onlynumbers.test(aadhar)){
        flag=false;
        message+="Aadhar field should only be having numeric values \n"
    }
    if(lname==""|| fname=="" || aadhar=="" || contact=="" || email=="" || address=="" || password==""){
        flag=false;
        message+="Empyt fields are not allowed\n"
    }

    // alert(message);
    if(flag){
        return true;
    }else{
        alert(message);
        return false;
    }
    
}
