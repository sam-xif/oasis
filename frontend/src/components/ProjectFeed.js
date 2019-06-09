import React from 'react';
import {Card, Button} from 'react-bootstrap'
import { Query } from 'react-apollo'
import gql from 'graphql-tag'
import {ProjectModal} from './ProjectModal';

const projectsQuery = gql`
  {
      projects {
          id
          name
          summary
          description
          lifecycle
          votes {
              type
          }
      }
  }
`

class ProjectFeedElement extends React.Component {
  render() {
    const {id, name, description, showProject} = this.props

    return <Card>
      <Card.Header>Featured</Card.Header>
      <Card.Body>
        <Card.Title>{name}</Card.Title>
        <Card.Text>
          {description}
        </Card.Text>
        <Button variant="primary" value={id} onClick={showProject}>Show Project</Button>
      </Card.Body>
    </Card>
  }
}

export default class ProjectFeed extends React.Component {
  state = {
    showProject: false,
    projectToShow: null,
  };


  showProject = event => {
      const id = event.target.value;
      this.setState({showProject: true, projectToShow: id})
  };

  hideProject = () => {
    this.setState({showProject: false})
  };

  render() {
      return (
      <Query query={projectsQuery}>
          {({ loading, error, data }) => {
              if (loading) return <div>Fetching</div>
              if (error) return <div>Error</div>

              const projects = data.projects
              const {projectToShow, showProject} = this.state;

              const projectsElements = projects.map(project => <ProjectFeedElement id={project.id} name={project.name} description={project.description} showProject={this.showProject}> </ProjectFeedElement>);

              const project = projects.find(el => {return el.id.toString() === projectToShow});
              const newProps = {...project, onHide: this.hideProject, show:showProject}
              const projectPopup = <ProjectModal {...newProps}/>;
              console.log({...newProps})

              return (
                  <div>
                      {projectsElements}
                      {projectPopup}
                  </div>
              );
          }}
      </Query>
      )
  }
}
