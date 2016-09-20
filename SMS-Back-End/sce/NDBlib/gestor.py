<!-- User projects section -->
             <div ng-if="vm.user.roles.pm">
                  <md-table-container>
                            <table md-table>
                                <thead md-head>
                                    <th md-column><span>As manager in projects:</span></th>
                                </thead>
                                <tbody md-body>
                                
                                <tr md-row ng-repeat="item in vm.user.roles.pm">

                                    <td md-cell>
                                    {{ item}}
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                  </md-table-container>
              </div>


              <div ng-if="vm.user.roles.dev">
                  <md-table-container>
                            <table md-table>
                                <thead md-head>
                                    <th md-column><span>As developer in projects:</span></th>
                                </thead>
                                <tbody md-body>
                                <!-- Where we iterate through items list -->
                                <tr md-row ng-repeat="item in vm.user.roles.dev">

                                    <td md-cell>
                                    {{ item}}
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                  </md-table-container>
              </div>
