import React from 'react'


export default function SignUpForm(props) {
  const [formData, setFormData] = React.useState({
    email: "",
    password: '',
    passwordConfirm: '',
    joinNewsletter: false
  })

  function handleSubmit(e) {
    e.preventDefault()

    if ( !formData.password || !formData.passwordConfirm ) {
      console.log('Must input a password')
    }
    else if ( formData.password !== formData.passwordConfirm ) {
      console.log('Passwords do not match')
    }
    else {
      console.log('Successfully signed up', formData)
    }
  }

  function handleChange(e) {
    const {name, value, type, checked} = e.target
    console.log('handleChange', name, value, type, checked)

    setFormData(prevFormData => {
      return {
        ...prevFormData,
        [name]: type === 'checkbox' ? checked : value
      }
    })
  }

  return (
    <form className="sign-up" onSubmit={handleSubmit}>
      <input name="email" type="email" value={formData.email.value} onChange={handleChange} placeholder="user@example.com" />
      <input name="password" type="password" value={formData.password.value} onChange={handleChange} placeholder="password" />
      <input name="passwordConfirm" type="password" value={formData.passwordConfirm.value} onChange={handleChange} placeholder="confirm password" />
      <label>
        <input name="joinNewsletter" type="checkbox" value={formData.joinNewsletter.value} onChange={handleChange} />
        I want to join the newsletter
      </label>
      <button>Sign Up</button>
    </form>
  )
}
