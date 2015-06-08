"""
 
Python Interchangeable Virtual Instrument Library
 
Copyright (c) 2012 Alex Forencich
 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
 
"""
 
import struct
 
from .. import ivi
from .. import scope
AcquisitionTypeMapping = {
        'normal': 'norm',
        'peak_detect': 'peak',
        'high_resolution': 'hres',
        'average': 'aver'}
VerticalCoupling = set(['ac', 'dc'])
TriggerTypeMapping = {
        'edge': 'edge',
        'width': 'glit',
        'glitch': 'glit',
        'tv': 'tv',
        #'immediate': '',
        'ac_line': 'edge',
        'pattern': 'patt',
        'can': 'can',
        'duration': 'dur',
        'i2s': 'i2s',
        'iic': 'iic',
        'eburst': 'ebur',
        'lin': 'lin',
        'm1553': 'm1553',
        'sequence': 'seq',
        'spi': 'spi',
        'uart': 'uart',
        'usb': 'usb',
        'flexray': 'flex'}
TriggerCouplingMapping = {
        'ac': ('ac', 0, 0),
        'dc': ('dc', 0, 0),
        'hf_reject': ('dc', 0, 1),
        'lf_reject': ('lfr', 0, 0),
        'noise_reject': ('dc', 1, 0),
        'hf_reject_ac': ('ac', 0, 1),
        'noise_reject_ac': ('ac', 1, 0),
        'hf_noise_reject': ('dc', 1, 1),
        'hf_noise_reject_ac': ('ac', 1, 1),
        'lf_noise_reject': ('lfr', 1, 0)}
TVTriggerEventMapping = {'field1': 'fie1',
        'field2': 'fie2',
        'any_field': 'afi',
        'any_line': 'alin',
        'line_number': 'lfi1',
        'vertical': 'vert',
        'line_field1': 'lfi1',
        'line_field2': 'lfi2',
        'line': 'line',
        'line_alternate': 'lalt',
        'lvertical': 'lver'}
TVTriggerFormatMapping = {'generic': 'gen',
        'ntsc': 'ntsc',
        'pal': 'pal',
        'palm': 'palm',
        'secam': 'sec',
        'p480l60hz': 'p480',
        'p480': 'p480',
        'p720l60hz': 'p720',
        'p720': 'p720',
        'p1080l24hz': 'p1080',
        'p1080': 'p1080',
        'p1080l25hz': 'p1080l25hz',
        'p1080l50hz': 'p1080l50hz',
        'p1080l60hz': 'p1080l60hz',
        'i1080l50hz': 'i1080l50hz',
        'i1080': 'i1080l50hz',
        'i1080l60hz': 'i1080l60hz'}
PolarityMapping = {'positive': 'pos',
        'negative': 'neg'}
GlitchConditionMapping = {'less_than': 'less',
        'greater_than': 'gre'}
WidthConditionMapping = {'within': 'rang'}
SampleModeMapping = {'real_time': 'rtim',
        'equivalent_time': 'etim',
        'segmented': 'segm'}
SlopeMapping = {
        'positive': 'pos',
        'negative': 'neg',
        'either': 'eith',
        'alternating': 'alt'}
MeasurementFunctionMapping = {
        'rise_time': 'risetime',
        'fall_time': 'falltime',
        'frequency': 'frequency',
        'period': 'period',
        'voltage_rms': 'vrms display',
        'voltage_peak_to_peak': 'vpp',
        'voltage_max': 'vmax',
        'voltage_min': 'vmin',
        'voltage_high': 'vtop',
        'voltage_low': 'vbase',
        'voltage_average': 'vaverage display',
        'width_negative': 'nwidth',
        'width_positive': 'pwidth',
        'duty_cycle_positive': 'dutycycle',
        'amplitude': 'vamplitude',
        'voltage_cycle_rms': 'vrms cycle',
        'voltage_cycle_average': 'vaverage cycle',
        'overshoot': 'overshoot',
        'preshoot': 'preshoot',
        'ratio': 'vratio',
        'phase': 'phase',
        'delay': 'delay'}
MeasurementFunctionMappingDigital = {
        'rise_time': 'risetime',
        'fall_time': 'falltime',
        'frequency': 'frequency',
        'period': 'period',
        'width_negative': 'nwidth',
        'width_positive': 'pwidth',
        'duty_cycle_positive': 'dutycycle'}
ScreenshotImageFormatMapping = {
        'bmp': 'bmp',
        'bmp24': 'bmp',
        'bmp8': 'bmp8bit',
        'png': 'png',
        'png24': 'png'}
TimebaseModeMapping = {
        'main': 'main',
        'window': 'wind',
        'xy': 'xy',
        'roll': 'roll'}
TimebaseReferenceMapping = {
        'left': 'left',
        'center': 'cent',
        'right': 'righ'}

# more instrument-specific sets and mappings
 
class rigolDS1054(ivi.Driver, scope.Base, scope.TVTrigger,
                scope.GlitchTrigger, scope.WidthTrigger, scope.AcLineTrigger,
                scope.WaveformMeasurement, scope.MinMaxWaveform,
                scope.ContinuousAcquisition, scope.AverageAcquisition,
                scope.SampleMode, scope.AutoSetup):
    "Agilent InfiniiVision 7000 series IVI oscilloscope driver"
 
    def __init__(self, *args, **kwargs):
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 0
        self._channel_label = list()
        # other per-channel instrument-specific variables that are
        # referenced in _init_channels
 
        super(rigolDS1054, self).__init__(*args, **kwargs)
 
        self._instrument_id = 'AGILENT TECHNOLOGIES'
        self._analog_channel_name = list()
        self._analog_channel_count = 4
        self._digital_channel_name = list()
        self._digital_channel_count = 0
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 1e9
        # initialize other instrument-specific variables
        
        self._channel_scale = list()

        self._identity_description = "Agilent InfiniiVision 7000 series IVI oscilloscope driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 4
        self._identity_specification_minor_version = 1
        self._horizontal_divisions = 10
        self._vertical_divisions = 8
        
        self._identity_supported_instrument_models =['']
 
        self.channels._add_property('label',
                        self._get_channel_label,
                        self._set_channel_label)
        
        self._add_property('display.labels',
                        self._get_display_labels,
                        self._set_display_labels,
                        None,
                        ivi.Doc("""
                        Turns the analog and digital channel labels on and off.
                        """))
        self._add_method('display.clear',
                        self._display_clear,
                        ivi.Doc("""
                        Clears the display and resets all associated measurements. If the
                        oscilloscope is stopped, all currently displayed data is erased. If the
                        oscilloscope is running, all the data in active channels and functions is
                        erased; however, new data is displayed on the next acquisition.
                        """))
        self._add_property('display.labels',
                        self._get_display_labels,
                        self._set_display_labels,
                        None,
                        ivi.Doc("""
                        Turns the analog and digital channel labels on and off.
                        """))
        self._add_property('channels[].scale',
                        self._get_channel_scale,
                        self._set_channel_scale,
                        None,
                        ivi.Doc("""
                        Specifies the vertical scale, or units per division, of the channel.  Units
                        are volts.
                        """))
        self._add_property('channels[].bw_limit',
                        self._get_channel_bw_limit,
                        self._set_channel_bw_limit,
                        None,
                        ivi.Doc("""
                        Commands an internal low-pass filter.  When the filter is on, the
                        bandwidth of the channel is limited to approximately 25 MHz.
                        """))
        # other instrument specific properties
 
        self._init_channels()
 
    def initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
 
        self._channel_count = self._analog_channel_count + self._digital_channel_count
 
        super(rigolDS1054, self).initialize(resource, id_query, reset, **keywargs)
 
        # interface clear
        if not self._driver_operation_simulate:
            self._clear()
 
        # check ID
        if id_query and not self._driver_operation_simulate:
            id = self.identity.instrument_model
            id_check = self._instrument_id
            id_short = id[:len(id_check)]
            if id_short != id_check:
                raise Exception("Instrument ID mismatch, expecting %s, got %s", id_check, id_short)
 
        # reset
        if reset:
            self.utility.reset()
 
 
    def _load_id_string(self):
        if self._driver_operation_simulate:
            self._identity_instrument_manufacturer = "Not available while simulating"
            self._identity_instrument_model = "Not available while simulating"
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            lst = self._ask("*IDN?").split(",")
            self._identity_instrument_manufacturer = lst[0]
            self._identity_instrument_model = lst[1]
            self._identity_instrument_firmware_revision = lst[3]
            self._set_cache_valid(True, 'identity_instrument_manufacturer')
            self._set_cache_valid(True, 'identity_instrument_model')
            self._set_cache_valid(True, 'identity_instrument_firmware_revision')
 
    def _get_identity_instrument_manufacturer(self):
        if self._get_cache_valid():
            return self._identity_instrument_manufacturer
        self._load_id_string()
        return self._identity_instrument_manufacturer
 
    def _get_identity_instrument_model(self):
        if self._get_cache_valid():
            return self._identity_instrument_model
        self._load_id_string()
        return self._identity_instrument_model
 
    def _get_identity_instrument_firmware_revision(self):
        if self._get_cache_valid():
            return self._identity_instrument_firmware_revision
        self._load_id_string()
        return self._identity_instrument_firmware_revision
 
    def _utility_disable(self):
        pass
 
    def _utility_error_query(self):
        error_code = 0
        error_message = "No error"
        if not self._driver_operation_simulate:
            error_code, error_message = self._ask(":system:error?").split(',')
            error_code = int(error_code)
            error_message = error_message.strip(' "')
        return (error_code, error_message)
 
    def _utility_lock_object(self):
        pass
 
    def _utility_reset(self):
        if not self._driver_operation_simulate:
            self._write("*RST")
            self.driver_operation.invalidate_all_attributes()
 
    def _utility_reset_with_defaults(self):
        self._utility_reset()
 
    def _utility_self_test(self):
        code = 0
        message = "Self test passed"
        if not self._driver_operation_simulate:
            code = int(self._ask("*TST?"))
            if code != 0:
                message = "Self test failed"
        return (code, message)
 
    def _utility_unlock_object(self):
        pass
 
    def _init_channels(self):
        try:
            super(rigolDS1054, self)._init_channels()
        except AttributeError:
            pass
        
        self._channel_name = list()
        self._channel_label = list()
        self._channel_probe_skew = list()
        self._channel_invert = list()
        self._channel_probe_id = list()
        self._channel_scale = list()
        self._channel_bw_limit = list()
        
        self._analog_channel_name = list()
        for i in range(self._analog_channel_count):
            self._channel_name.append("channel%d" % (i+1))
            self._channel_label.append("%d" % (i+1))
            self._analog_channel_name.append("channel%d" % (i+1))
            self._channel_probe_skew.append(0)
            self._channel_scale.append(1.0)
            self._channel_invert.append(False)
            self._channel_probe_id.append("NONE")
            self._channel_bw_limit.append(False)
        
        # digital channels
        self._digital_channel_name = list()
        if (self._digital_channel_count > 0):
            for i in range(self._digital_channel_count):
                self._channel_name.append("digital%d" % i)
                self._channel_label.append("D%d" % i)
                self._digital_channel_name.append("digital%d" % i)
            
            for i in range(self._analog_channel_count, self._channel_count):
                self._channel_input_impedance[i] = 100000
                self._channel_input_frequency_max[i] = 1e9
                self._channel_probe_attenuation[i] = 1
                self._channel_coupling[i] = 'dc'
                self._channel_offset[i] = 0
                self._channel_range[i] = 1
        
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self.channels._set_list(self._channel_name)
 
    def _get_acquisition_start_time(self):
        pos = 0
        if not self._driver_operation_simulate and not self._get_cache_valid():
            pos = float(self._ask(":timebase:position?"))
            self._set_cache_valid()
        self._acquisition_start_time = pos - self._get_acquisition_time_per_record() * 5 / 10
        return self._acquisition_start_time
 
    def _set_acquisition_start_time(self, value):
        value = float(value)
        value = value + self._get_acquisition_time_per_record() * 5 / 10
        if not self._driver_operation_simulate:
            self._write(":timebase:position %e" % value)
        self._acquisition_start_time = value
        self._set_cache_valid()
        
    def _get_acquisition_time_per_record(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_time_per_record = float(self._ask(":timebase:range?"))
            self._set_cache_valid()
        return self._acquisition_time_per_record
    
    def _set_acquisition_time_per_record(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":timebase:range %e" % value)
        self._acquisition_time_per_record = value
        self._set_cache_valid()
        self._set_cache_valid(False, 'acquisition_start_time')
        
    def _get_channel_label(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_label[index] = self._ask(":%s:label?" % self._channel_name[index]).strip('"')
            self._set_cache_valid(index=index)
        return self._channel_label[index]
    
    def _set_channel_label(self, index, value):
        print('_set_channel_label', index, value)
        value = str(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write(":%s:label \"%s\"" % (self._channel_name[index], value))
        self._channel_label[index] = value
        self._set_cache_valid(index=index)
        
    def _get_channel_enabled(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_enabled[index] = bool(int(self._ask(":%s:display?" % self._channel_name[index])))
            self._set_cache_valid(index=index)
        return self._channel_enabled[index]
    
    def _set_channel_enabled(self, index, value):
        value = bool(value)
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate:
            self._write(":%s:display %d" % (self._channel_name[index], int(value)))
        self._channel_enabled[index] = value
        self._set_cache_valid(index=index)
        
    def _display_clear(self):
        if not self._driver_operation_simulate:
            self._write(":cdisplay")
            
    def _get_display_labels(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._display_labels = bool(int(self._ask(":display:label?")))
            self._set_cache_valid()
        return self._display_labels
    
    def _set_display_labels(self, value):
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":display:label %d" % int(value))
        self._display_labels = value
        self._set_cache_valid()
        
    def _get_trigger_coupling(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            cpl = self._ask(":trigger:coupling?").lower()
            noise = int(self._ask(":trigger:nreject?"))
            hf = int(self._ask(":trigger:hfreject?"))
            for k in TriggerCouplingMapping:
                if (cpl, noise, hf) == TriggerCouplingMapping[k]:
                    self._trigger_coupling = k
        return self._trigger_coupling
    
    def _set_trigger_coupling(self, value):
        if value not in TriggerCouplingMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            cpl, noise, hf = TriggerCouplingMapping[value]
            self._write(":trigger:coupling %s" % cpl)
            self._write(":trigger:nreject %d" % noise)
            self._write(":trigger:hfreject %d" % hf)
        self._trigger_coupling = value
        self._set_cache_valid()
        
    def _get_channel_bw_limit(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_bw_limit[index] = bool(int(self._ask(":%s:bwlimit?" % self._channel_name[index])))
            self._set_cache_valid(index=index)
        return self._channel_bw_limit[index]
    
    def _set_channel_bw_limit(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":%s:bwlimit %d" % (self._channel_name[index], int(value)))
        self._channel_bw_limit[index] = value
        self._set_cache_valid(index=index)
        
    def _get_channel_coupling(self, index):
        print("_get_channel_coupling", self._analog_channel_name)
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_coupling[index] = self._ask(":%s:coupling?" % self._channel_name[index]).lower()
            self._set_cache_valid(index=index)
        return self._channel_coupling[index]
    
    def _set_channel_coupling(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        if value not in VerticalCoupling:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":%s:coupling %s" % (self._channel_name[index], value))
        self._channel_coupling[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_offset(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_offset[index] = float(self._ask(":%s:offset?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_offset[index]
    
    def _set_channel_offset(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:offset %e" % (self._channel_name[index], value))
        self._channel_offset[index] = value
        self._set_cache_valid(index=index)
    
    def _get_channel_range(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_range[index] = float(self._ask(":%s:range?" % self._channel_name[index]))
            self._channel_scale[index] = self._channel_range[index] / self._vertical_divisions
            self._set_cache_valid(index=index)
            self._set_cache_valid(True, "channel_scale", index)
        return self._channel_range[index]
    
    def _set_channel_range(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:range %e" % (self._channel_name[index], value))
        self._channel_range[index] = value
        self._channel_scale[index] = value / self._vertical_divisions
        self._set_cache_valid(index=index)
        self._set_cache_valid(True, "channel_scale", index)
    
    def _get_channel_scale(self, index):
        index = ivi.get_index(self._channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_scale[index] = float(self._ask(":%s:scale?" % self._channel_name[index]))
            self._channel_range[index] = self._channel_scale[index] * self._vertical_divisions
            self._set_cache_valid(index=index)
            self._set_cache_valid(True, "channel_range", index)
        return self._channel_scale[index]
    
    def _set_channel_scale(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:scale %e" % (self._channel_name[index], value))
        self._channel_scale[index] = value
        self._channel_range[index] = value * self._vertical_divisions
        self._set_cache_valid(index=index)
        self._set_cache_valid(True, "channel_range", index)
    
    def _get_measurement_status(self):
        return self._measurement_status
    
    # more definitions