======================
Low Latency - Examples
======================

These test examples outline comprehensive test scenarios that can be used to
run *Low Latency* tests by the means of the ByteBlower Test Framework. A test
is designed to assess the performance and robustness of networks,
incorporating `Stateless`_ Frame Blasting-based and `Stateful`_ HTTP flows.

.. _Stateless: https://support.excentis.com/knowledge/article/85
.. _Stateful: https://support.excentis.com/knowledge/article/86

Additionally, we provide other frame blasting-based flows to form the base of
*application simulation*, such as:

* Voice calls:
  :py:class:`~byteblower_test_framework.traffic.VoiceFlow`
* Video streaming:
  :py:class:`~byteblower_test_framework.traffic.VideoFlow`
* (traditional) gaming:
  :py:class:`~byteblower_test_framework.traffic.GamingFlow`
* Video Conference calls that includes: Video, voice, and screen sharing

This configuration is tailored to simulate realistic traffic patterns between
a typical service provider (NSI) and customer premise equipment (CPE), and
measuring key network metrics. This test is particularly valuable for Internet
Service Providers (ISPs), network equipment manufacturers, and large
organizations with intricate network infrastructures that demand very low
latency and high levels of reliability and speed.

A test scenario is versatile and can be employed to:

- *Validate Quality of Service (QoS) and Quality of Experience (QoE)*: It
  helps in ensuring that the network can handle varied types of traffic with
  specific quality requirements, which is crucial for service providers aiming
  to guarantee service level agreements (SLAs).

- *Benchmark Network Performance*: By testing with different frame sizes,
  rates, and protocols, network administrators can understand the performance
  boundaries of their networks and identify potential bottlenecks.

- *Simulate Real-World Traffic*: The configuration allows for simulating
  different types of traffic (e.g., UDP-based, HTTP), thereby providing
  insights into how a network would perform under typical or peak usage
  conditions.

- *Network Optimization and Planning*: The detailed analysis and reporting
  enable network engineers to make data-driven decisions for capacity planning
  and network optimization.

- *Troubleshooting and Diagnostics*: By highlighting packet loss, latency
  issues, and the behavior of the network under high load, the tests can
  pinpoint issues that need to be addressed to prevent future outages or
  performance degradation.


You can find here some examples that you can use easily to run your tests, in
addition to detailed guidelines on how to use them, what results to expect,
and how to interpret these results.

Ready to start? You need only to choose which example to go with!

.. toctree::
   :maxdepth: 1

   Basic <basic>
   L4S <l4s>

.. ! FIXME: Putting ``tags`` *before* ``toctree`` messes up
.. !        the tracking in the navigation sidebar

.. tags:: Introduction
