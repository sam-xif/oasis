import React from 'react';
import '../styles/App.css';
import {Card, Button, Modal} from 'react-bootstrap'
import {client} from '../index.js'
import { Query } from 'react-apollo'
import gql from 'graphql-tag'



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



class ProjectTableElement extends React.Component {
  render() {
    const {id, name, description, showProject} = this.props

    return <Card>
      <Card.Header>Featured</Card.Header>
      <Card.Body>
        <Card.Title>{name}</Card.Title>
        <Card.Text>
          {description}
        </Card.Text>
        <Button variant="primary" value={id} onClick={ showProject}>Show Project</Button>
      </Card.Body>
    </Card>
  }
}

class Project extends React.Component {
  render() {
    const {name, description, lifecycle, onHide} = this.props;
    console.log(this.props);
    return <Modal
        {...this.props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered>
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          {name}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <ul>
          <li>Description: {description}</li>
          <li>Lifecycle status: {lifecycle}</li>
        </ul>
      </Modal.Body>
      <Modal.Footer>
        <Button onClick={onHide}>Close</Button>
      </Modal.Footer>
    </Modal>
  }
}


class ProjectTable extends React.Component {
  state = {
    //showProject: false,
    //projectToShow: 1
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

              const projectsElements = projects.map(project => <ProjectTableElement id={project.id} name={project.name} description={project.description} showProject={this.showProject}> </ProjectTableElement>);
              const project = projects.find(el => {return el.id == projectToShow});
              const newProps = {...project, onHide: this.hideProject, show:showProject}
              const projectPopup = <Project {...newProps}/>;
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

class App extends React.Component {
  render() {
    return <ProjectTable/>
  }
}

export default App;
