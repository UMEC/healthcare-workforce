import React from 'react'
import { Accordion } from 'semantic-ui-react'

let rootPanels = (props) => {
  let results = [];
  {props.contents.forEach((content) => {
    console.log("Looking at content: " + content.key);
    results.push({ key: content.key, title: content.title, content: { content: content.value } });
  })}
  return results;
}

const AccordionExampleNested = (props) => <Accordion defaultActiveIndex={0} panels={rootPanels(props)} styled />

export default AccordionExampleNested