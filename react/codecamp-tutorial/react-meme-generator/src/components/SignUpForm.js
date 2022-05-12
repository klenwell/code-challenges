import React from 'react'


export default function SignUpForm(props) {
  const [formData, setFormData] = React.useState({
    email: "",
    password: '',
    pw_confirm: '',
    newsletter: false
  })

  function handleSubmit(e) {
    e.preventDefault()

    if ( !formData.password || !formData.pw_confirm ) {
      console.log('Must input a password')
    }
    else if ( formData.password !== formData.pw_confirm ) {
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
      <input name="pw_confirm" type="password" value={formData.pw_confirm.value} onChange={handleChange} placeholder="confirm password" />
      <label>
        <input name="newsletter" type="checkbox" value={formData.newsletter.value} onChange={handleChange} />
        I want to join the newsletter
      </label>
      <button>Sign Up</button>
    </form>
  )
}
