import React, { useState } from 'react';
import { useOutletContext } from 'react-router-dom';
// eslint-disable-next-line no-unused-vars
import axios from 'axios';
import './pages.css';
import ScheduleList from './ScheduleList';

const Schedule = () => {
  const {
    addressData,
    setAddressData,
    directionsRequest,
    setDirectionsRequest,
  } = useOutletContext()[0];
  //console.log(addressData);
  const [dayOfWeek, setDayOfWeek] = useState(new Array(7).fill(false));
  const [scheduledOrigin, setScheduledOrigin] = useState('');
  const [scheduledDestination, setScheduledDestination] = useState('');
  const [scheduledTravelMode, setScheduledTravelMode] = useState('TRANSIT');
  const [departArrive, setDepartArrive] = useState('');
  const [scheduledTime, setScheduledTime] = useState('');
  // eslint-disable-next-line no-unused-vars
  const [errorMessageRoute, setErrorMessageRoute] = useState('');

  const [scheduledDirections, setScheduledDirecitons] = useState([]);

  // Autocomplete useStates and useRefs
  const [showOriginDropdown, setShowOriginDropdown] = useState(false);
  const [showDestDropdown, setShowDestDropdown] = useState(false);

  const onSubmitRoute = () => {
    // Make sure valid days are chosen. If no days are chosen return error
    let validDays = false;
    dayOfWeek.map((day) => {
      if (day === true) validDays = true;
    });
    if (validDays) {
      if (scheduledOrigin && scheduledDestination) {
        axios({
          method: 'POST',
          url: '/save_scheduled_directions',
          headers: {
            // checks if user is authorized to set data
            Authorization: 'Bearer ' + localStorage.getItem('token'),
          },
          data: {
            scheduledTravelMode: scheduledTravelMode,
            departArrive: departArrive,
            scheduledTime: scheduledTime,
            scheduledOrigin: scheduledOrigin,
            scheduledDestination: scheduledDestination,
            dayOfWeek: dayOfWeek,
          },
        })
          .then((response) => {
            console.log(response);
            setErrorMessageRoute('SUCCESSFULLY ADDED ROUTE TO SCHEDULE!');
          })
          .catch((error) => {
            if (error.response) {
              setErrorMessageRoute('FAILED TO SAVE ROUTE! TRY AGAIN.');
              console.log(error.response);
              console.log(error.response.status);
              console.log(error.response.headers);
            }
          });
        setScheduledDirecitons(scheduledDirections);
      } else {
        setErrorMessageRoute('BE SURE TO CHOOSE AN ORIGIN AND A DESTINATION!');
      }
    } else {
      setErrorMessageRoute('BE SURE TO ADD YOUR ROUTE TO A DAY OF THE WEEK!');
    }
  };

  // The logic for the checkbox onChange function is weird but it works.
  // By nesting the onChange function inside the getOnChangeWithIndex function
  // we can run the inner logic ONCE on each click. If the logic isn't nested then
  // getOnChangeWithIndex will run on render and then rerender constantly
  const getOnChangeWithIndex = (day) => {
    const onChange = () => {
      let newDayOfWeek = [...dayOfWeek];
      newDayOfWeek[day] = !dayOfWeek[day];
      setDayOfWeek(newDayOfWeek);
    };
    return onChange;
  };
  const onOriginChange = (event) => {
    setScheduledOrigin(event.target.value);
  };
  const onDestinationChange = (event) => {
    setScheduledDestination(event.target.value);
  };
  const onTravelModeChange = (event) => {
    setScheduledTravelMode(event.target.value);
  };
  const onDepartArriveChange = (event) => {
    setDepartArrive(event.target.value);
  };
  const onScheduledTimeChange = (event) => {
    setScheduledTime(event.target.value);
  };

  return (
    <div id='scheduleSection'>
      <h2>Weekly Schedule</h2>
      <ul id='weeklySchedule'></ul>
      <p>Add a route to your weekly schedule:</p>
      <input
        type='checkbox'
        id='Monday'
        name='day'
        value='0'
        onChange={getOnChangeWithIndex(0)}
      ></input>
      <label htmlFor='Monday'>Monday</label>
      <input
        type='checkbox'
        id='Tuesday'
        name='day'
        value='Tuesday'
        onChange={getOnChangeWithIndex(1)}
      ></input>
      <label htmlFor='Tuesday'>Tuesday</label>
      <input
        type='checkbox'
        id='Wednesday'
        name='day'
        value='Wednesday'
        onChange={getOnChangeWithIndex(2)}
      ></input>
      <label htmlFor='Wednesday'>Wednesday</label>
      <input
        type='checkbox'
        id='Thursday'
        name='day'
        value='Thursday'
        onChange={getOnChangeWithIndex(3)}
      ></input>
      <label htmlFor='Thursday'>Thursday</label>
      <input
        type='checkbox'
        id='Friday'
        name='day'
        value='Friday'
        onChange={getOnChangeWithIndex(4)}
      ></input>
      <label htmlFor='Friday'>Friday</label>
      <input
        type='checkbox'
        id='Saturday'
        name='Saturday'
        value='Saturday'
        onChange={getOnChangeWithIndex(5)}
      ></input>
      <label htmlFor='Saturday'>Saturday</label>
      <input
        type='checkbox'
        id='Sunday'
        name='day'
        value='Sunday'
        onChange={getOnChangeWithIndex(6)}
      ></input>
      <label htmlFor='Sunday'>Sunday</label>
      <br />
      <div className='fieldWrapper'>
        <label htmlFor='from'>Origin </label>
        <input
          type='text'
          id='from'
          placeholder='enter address'
          value={scheduledOrigin}
          onChange={onOriginChange}
          onFocus={() => setShowOriginDropdown(true)}
          onBlur={(e) => {
            console.log(e.relatedTarget);
            if (
              !e.relatedTarget ||
              !e.relatedTarget.classList.contains('addressDropdown')
            )
              setShowOriginDropdown(false);
          }}
        ></input>
        {showOriginDropdown && (
          <div className='addressDropdown' tabIndex={'-1'}>
            {addressData && addressData.length > 0 && (
              <>
                {addressData.map((address, index) => (
                  <div
                    key={'address_' + index}
                    className='addressItem'
                    onClick={() => {
                      setScheduledOrigin(address);
                      setShowOriginDropdown(false);
                    }}
                  >
                    {address}
                  </div>
                ))}
              </>
            )}
          </div>
        )}
      </div>
      <div className='fieldWrapper'>
        <label htmlFor='dest'>Destination </label>
        <input
          type='text'
          id='dest'
          placeholder='enter address'
          value={scheduledDestination}
          onChange={onDestinationChange}
          onFocus={() => setShowDestDropdown(true)}
          onBlur={(e) => {
            console.log(e.relatedTarget);
            if (
              !e.relatedTarget ||
              !e.relatedTarget.classList.contains('addressDropdown')
            )
              setShowDestDropdown(false);
          }}
        ></input>
        {showDestDropdown && (
          <div className='addressDropdown' tabIndex={'-1'}>
            {addressData && addressData.length > 0 && (
              <>
                {addressData.map((address, index) => (
                  <div
                    key={'address_' + index}
                    className='addressItem'
                    onClick={() => {
                      setScheduledDestination(address);
                      setShowDestDropdown(false);
                    }}
                  >
                    {address}
                  </div>
                ))}
              </>
            )}
          </div>
        )}
      </div>
      <b className='commute'>Select Type of Commute </b>
      <select
        id='mode'
        value={scheduledTravelMode}
        onChange={onTravelModeChange}
      >
        <option value='DRIVING'>Driving</option>
        <option value='WALKING'>Walking</option>
        <option value='BICYCLING'>Bicycling</option>
        <option value='TRANSIT' selected>
          Transit
        </option>
      </select>
      <br />
      <label htmlFor='scheduleTime'>Departure or Arrival Time? </label>
      <select
        id='scheduleTime'
        value={departArrive}
        onChange={onDepartArriveChange}
      >
        <option value=''>-- </option>
        <option value='DEPART'>Departure </option>
        <option value='ARRIVE'>Arrival </option>
      </select>
      <label htmlFor='scheduleArrive'> Time </label>
      <input
        type='time'
        id='scheduleArrive'
        onChange={onScheduledTimeChange}
      ></input>
      <button id='save' onClick={onSubmitRoute}>
        Save
      </button>
      {errorMessageRoute && <p className='error'> {errorMessageRoute} </p>}
      <ScheduleList
        directionsRequest={directionsRequest}
        setDirectionsRequest={setDirectionsRequest}
      />
    </div>
  );
};
export default Schedule;
