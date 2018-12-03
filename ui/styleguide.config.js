module.exports = {
  // components: 'src/components/**/[A-Z]*.js',
  sections: [
    { 
      name: 'components', 
      description: 'Components are individual pieces of the UI (user interface) broken out into reusable modules; they should render based on props passed down to them. They do not call any APIs',
      components: 'src/components/**/[A-Z]*.js'
    },
    {
      name: 'containers',
      description: 'Containers are concerned with logic and data consumption.',
      components: 'src/containers/**/[A-Z]*.js'
    },
    { name: 'reducers', content: 'src/reducers/README.md', components: 'src/reducers/**/[A-Z]*.js'},
  ]
}