import React from "react";
import useForm from "react-hook-form";
import userWallet from '../helpers/wallet';

function Form() {
    const { register, handleSubmit, errors } = useForm();
    const onSubmit = data => {
      userWallet()
    console.log(data);
    };

    return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input name="id" defaultValue="Brian" ref={register({ required: true })} /> 
      <input type="submit" />
      {errors.id && 'You need to enter an existing username'}
    </form>
    );
}

export default Form;