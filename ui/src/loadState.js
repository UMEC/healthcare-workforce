export const loadStateFromLocalStorage = () => {
  // Wrapping in a try catch to prevent any issues when an error is returned 
  try {
    const serializedState = localStorage.getItem('state');

    // If there is no state in the localStorage, return `undefined` and continue
    // running as ususal
    if ( serializedState === null ) return undefined;

    // If there is a state key in Localstorage, parse it and return it to be applied to the 
    return JSON.parse(serializedState);
  } catch (error) {
    return undefined
  }
}

export const saveStateToLocalStorage = (state) => {
  try {
    const serializedState = JSON.stringify(state);
    localStorage.setItem('state', serializedState);
  } catch (error) {
    console.log('saveStateToLocalStorage', error)
  }
}
export const loadStateFromSessionStorage = () => {
  // Wrapping in a try catch to prevent any issues when an error is returned 
  try {
    const serializedState = sessionStorage.getItem('state');

    // If there is no state in the localStorage, return `undefined` and continue
    // running as ususal
    if ( serializedState === null ) return undefined;

    // If there is a state key in Localstorage, parse it and return it to be applied to the 
    return JSON.parse(serializedState);
  } catch (error) {
    return undefined
  }
}

export const saveStateToSessionStorage = (state) => {
  try {
    const serializedState = JSON.stringify(state);
    sessionStorage.setItem('state', serializedState);
  } catch (error) {
    console.log('saveStateToSessionStorage', error)
  }
}

/***
 * Based on a great video by Dan Abermov.
 * https://egghead.io/lessons/javascript-redux-persisting-the-state-to-the-local-storage
 * 
 * Note about Keys: 
 * Dan mentions that this could cause issues when using an incramented value (e.g. incramenting a variable of `id = 0` )
 * This can be solved by using a package called `node-uuid` for unique keys
 * 
 */