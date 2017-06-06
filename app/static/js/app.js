

class Sidebar extends React.Component{
  constructor(props){
    super(props)
  }


  test(r){
    console.log(r)
  }

  render(){
    // count = this.props.count

    var routesList = this.props.routes.map(function(route){
      return <a href="#" className="list-group-item">{route.name}</a>
    })



    return(
    <div className="list-group">
      <a href="#" className="list-group-item active" onClick={this.test(454)}>
        Маршрути {this.props.routes.count}
      </a>
     
      {routesList}

    </div>

    )
  }
}








class App extends React.Component{
  constructor(props){
    super(props)

    this.state = {
      count: 0,
      routes: []
    }
  }


  fetchRoutes(){
    var url = document.URL + 'api/routes'

    fetch(url).then(function(response){
      return response.json()
    }).then(function(response){
      console.log(response)
      this.setState({
        count: response.count,
        routes: response.routes
      })
    }.bind(this))

  }


  componentDidMount(){
    this.fetchRoutes()
  }


  render(){
    console.log(this.state)
    return(
      <div className="row">
        <div className="col-sm-4">
          <Sidebar routes={this.state.routes} />
        </div>
        <div className="col-sm-8">
          <button onClick={this.fetchRoutes}>Fetch</button>
        </div>
      </div>
    )
  }
}

ReactDOM.render(<App/>,document.getElementById('app'))
