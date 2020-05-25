/*
This file contains a template for testing components in React.
For more info: https://reactjs.org/docs/testing-recipes.html#setup--teardown
and https://create-react-app.dev/docs/running-tests. 
*/

import React from 'react';
import { unmountComponentAtNode, render } from 'react-dom';
import { act } from 'react-dom/test-utils';
// Import here the component that you wish to test.

export default function Hello(props) {
    if (props.name) {
      return <h1>Hello, {props.name}!</h1>;
    } else {
      return <span>Hey, stranger</span>;
    }
  }

let container = null;

/**
 * For each test, we usually want to render our React tree to a DOM element 
 * that’s attached to document. 
 */
beforeEach(() => {
    // Setup a DOM element as a render target
    container = document.createElement("div");
    document.body.appendChild(container); 
});

/**
 * When the test ends, clean up and unmount the tree from the document.
 */
afterEach(() => {
    // Clean up on exiting
    unmountComponentAtNode(container);
    container.remove();
    container = null;
});

/**
 * Function containing a lot of tests. We first render the component with 'act'
 * and then, outside of 'act' we assert. It can be called 'it()' or 'test()'
 */
it("Name of the test", () => {
    act(() => {
        // Render components
        render(<Hello />, container); 
    });
    // Assert and check whether the result was as expected.
    expect(container.textContent).toBe("Hey, stranger"); 
    // There are many expect functions. It comes from Jest: https://jestjs.io/docs/en/expect.html#content
});