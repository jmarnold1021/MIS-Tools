DROP TABLE [dbo].[L56_NscDetailFileStage]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_NscDetailFileStage]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[L56_NscDetailFileStage](
	[SSN] [varchar](16) NULL,
	[FirstName] [varchar](20) NULL,
	[MiddleInitial] [varchar](1) NULL,
	[LastName] [varchar](20) NULL,
	[Suffix] [varchar](5) NULL,
	[RequesterReturnField] [varchar](50) NOT NULL,
	[RecordFound] [varchar](1) NULL,
	[SearchDate] [varchar](8) NULL,
	[CollegeCode] [varchar](9) NULL,
	[CollegeName] [varchar](50) NULL,
	[CollegeState] [varchar](2) NULL,
	[CollegeType] [varchar](1) NULL,
	[CollegePublicPrivate] [varchar](7) NULL,
	[EnrollmentBegin] [varchar](8) NULL,
	[EnrollmentEnd] [varchar](8) NULL,
	[EnrollmentStatus] [varchar](1) NULL,
	[ClassLevel] [varchar](1) NULL,
	[Major1] [varchar](80) NULL,
	[Cip1] [varchar](6) NULL,
	[Major2] [varchar](80) NULL,
	[Cip2] [varchar](6) NULL,
	[Graduated] [varchar](1) NULL,
	[GraduationDate] [varchar](8) NULL,
	[DegreeTitle] [varchar](80) NULL,
	[DegreeMajor1] [varchar](80) NULL,
	[DegreeCip1] [varchar](6) NULL,
	[DegreeMajor2] [varchar](80) NULL,
	[DegreeCip2] [varchar](6) NULL,
	[DegreeMajor3] [varchar](80) NULL,
	[DegreeCip3] [varchar](6) NULL,
	[DegreeMajor4] [varchar](80) NULL,
	[DegreeCip4] [varchar](6) NULL,
	[CollegeSequence] [varchar](2) NULL
) ON [PRIMARY]
END
GO
