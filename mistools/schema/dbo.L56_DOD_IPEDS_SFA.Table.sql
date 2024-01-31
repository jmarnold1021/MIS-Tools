DROP TABLE [dbo].[L56_DOD_IPEDS_SFA]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_IPEDS_SFA]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[L56_DOD_IPEDS_SFA](
	[COLLEGE_ID] [varchar](3) NULL,
	[STUDENT_ID] [varchar](9) NOT NULL,
	[TERM_ID] [varchar](3) NULL,
	[TYPE_ID] [varchar](2) NOT NULL,
	[ENROLLMENT] [varchar](1) NULL,
	[UNITS_ATTEMPTED] [decimal](6, 2) NULL,
	[DEGREE_FLAG] [varchar](1) NULL,
	[RESIDENCY] [varchar](2) NULL,
	[YR] [varchar](4) NULL,
	[AWARD_STATUS] [varchar](1) NULL,
	[AWARD_AMOUNT] [int] NULL,
	[BUDGET_CATEGORY] [varchar](1) NULL,
	[INCOME] [int] NULL,
	[YEAR] [varchar](4) NOT NULL,
	[LATTER_YEAR] [varchar](4) NOT NULL,
 CONSTRAINT [PK_DOD_IPEDS_LATTER_YEAR_YEAR_TYPE_ID_STUDENT_ID] PRIMARY KEY CLUSTERED 
(
	[LATTER_YEAR] DESC,
	[YEAR] DESC,
	[STUDENT_ID] ASC,
	[TYPE_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
END
GO
